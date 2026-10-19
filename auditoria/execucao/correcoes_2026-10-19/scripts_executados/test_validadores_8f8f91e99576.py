"""Regressões de conteúdo, camadas e empacotamento, sem editar artes aprovadas."""
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import contrato_bellas as contract
import validar_manifest as manifest
import validar_artefatos_bellas as artifacts
import verificar_textos_psd as texts
import empacotar as pack
import registrar_reabertura as registration
from PIL import Image
MISSING = object()


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "base.psd").write_bytes(b"fixture de caminho, nao um PSD real")
        (self.root / "fonte.txt").write_text("Treinamento\nConteudo original", encoding="utf-8")
        self.path = self.root / "manifesto.json"
        self.addCleanup(patch.stopall)
        patch.object(contract, "ROOT", self.root).start()
        patch.object(contract, "APPROVED", self.root / "base.psd").start()
        patch.object(manifest, "APPROVED_TEMPLATE", self.root / "base.psd").start()
        self.data = {"schema_version":"2.0", "stage":"final", "canvas":[1920,1080], "template":{"psd":"base.psd"},
            "sources":[{"id":"title", "file":"fonte.txt", "page":1, "text":"Treinamento"}, {"id":"body", "file":"fonte.txt", "page":2, "text":"Conteudo original"}],
            "slides":[
                {"number":1,"group":"01 - Capa","fixed":"cover","theme":"claro","elements":[self.element("title","h1","Treinamento","title")]},
                {"number":2,"group":"02 - Conteudo","theme":"escuro","elements":[self.element("heading","h1","Conteudo","body"),self.element("body","body","Conteudo original","body")]},
                {"number":3,"group":"03 - Obrigada","fixed":"thanks","theme":"claro","elements":[]}]}

    def element(self, eid, role, text, source):
        return {"id":eid,"role":role,"text":text,"rect":[.1,.2,.8,.2],"layer":"CONTENT/"+eid,"font":"Gotham-Book","color":"FFFFFF","source_ids":[source]}

    def validate(self, data=MISSING, **kwargs):
        self.path.write_text(json.dumps(self.data if data is MISSING else data),encoding="utf-8")
        return manifest.validate(self.path, "final", True, **kwargs)

    def test_valid_final(self):
        self.assertEqual(self.validate(), [])

    def test_five_regressions_cannot_pass(self):
        mutations = [lambda d:d.pop("sources"), lambda d:d["slides"][0]["elements"].append(self.element("extra","body","Chamada comercial","title")), lambda d:d["slides"][1]["elements"][1].update(text="TEXTO\n5–6 LINHAS\nLOREM IPSUM"), lambda d:d["slides"][1]["elements"][1].update(font="Arial",color="000000"), lambda d:d["slides"][-1].update(fixed="cover",elements=[self.element("wrong","h1","Outro encerramento","body")])]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = deepcopy(self.data)
                mutation(data)
                self.assertTrue(self.validate(data))

    def test_placeholder_detection_preserves_real_sentences(self):
        for text in ["TEXTO", "5-6 LINHAS", "5–6 LINHAS", "5—6 LINHAS", "Inserir foto", "H1", "ITEM 02", "lorem ipsum"]:
            self.assertIsNotNone(contract.TEMP_LABEL.search(text), text)
        for text in ["Item essencial para começar", "Texto de apoio legível", "O título explica o assunto"]:
            self.assertIsNone(contract.TEMP_LABEL.search(text), text)

    def test_final_stage_not_inferred_from_cli_only(self):
        self.data["stage"] = "planejamento"
        self.assertTrue(self.validate())

    def test_coverage_unknown_duplicate_and_omitted_sources(self):
        self.data["sources"].append({"id":"extra","file":"fonte.txt","page":3,"text":"Ressalva"})
        self.assertTrue(self.validate())
        self.data["omitted_sources"] = [{"id":"extra","reason":"Decisão editorial documentada"}]
        self.assertEqual(self.validate(),[])
        self.data["slides"][1]["elements"][1]["source_ids"] = ["inexistente"]
        self.assertTrue(self.validate())

    def test_source_path_cannot_leave_package(self):
        self.data["sources"][0]["file"] = "../fora.txt"
        self.assertTrue(self.validate())

    def test_layer_and_group_uniqueness(self):
        self.data["slides"][1]["elements"][1]["layer"] = "CONTENT/heading"
        self.assertTrue(self.validate())

    def test_mixed_styles_and_body_color(self):
        self.data["slides"][1]["elements"][0]["runs"] = [{"start":0,"end":3,"font":"Gotham-Bold","color":"B3718E"}]
        self.assertEqual(self.validate(),[])
        self.data["slides"][1]["elements"][1]["runs"] = [{"start":0,"end":3,"color":"000000"}]
        self.assertTrue(self.validate())

    def test_historical_mode_explicit(self):
        data = deepcopy(self.data)
        data["schema_version"] = "1.0"
        data["slides"] = data["slides"][:2]
        data.pop("sources")
        self.assertTrue(self.validate(data))
        self.assertEqual(self.validate(data, legacy=True),[])

    def test_malformed_input_is_rejected(self):
        for value in [None, [], {"template":{}}, {"slides":[],"canvas":None}]:
            with self.subTest(value=value):
                self.assertTrue(self.validate(value))


class Layer:
    def __init__(self, name, text=None, children=None, visible=True, font="Gotham-Book", color=(1,1,1)):
        self.name,self.text,self.children,self.visible = name,text,children,visible
        self.kind = "group" if children is not None else "type"
        self.resource_dict = {"FontSet":[{"Name":font}]}
        self.engine_dict = {"StyleRun":{"RunLengthArray":[len((text or "").encode("utf-16-le"))//2+1],"RunArray":[{"StyleSheet":{"StyleSheetData":{"Font":0,"FillColor":{"Values":[1,*color]}}}}]}}
    def __iter__(self):
        return iter(self.children or [])
    def is_group(self):
        return self.children is not None


class PSDLinkTests(unittest.TestCase):
    def setUp(self):
        self.layer = Layer("H1","Mensagem real")
        self.content = Layer("CONTENT",children=[self.layer])
        self.page = Layer("01 - Tema",children=[self.content],visible=False)
        self.el = {"id":"t","role":"h1","layer":"CONTENT/H1","text":"Mensagem real","font":"Gotham-Book","color":"FFFFFF"}
        self.data = {"slides":[{"number":1,"group":"01 - Tema","elements":[self.el]}]}
    def test_exact_layer_text_style_and_hidden_page(self):
        self.assertEqual(texts.compare_pages(self.data,[self.page]),[])
    def test_text_mutation_is_detected(self):
        self.el["text"] = "Mensagem inventada"
        self.assertTrue(texts.compare_pages(self.data,[self.page]))
    def test_wrong_font_and_color_are_detected(self):
        self.layer.resource_dict["FontSet"][0]["Name"] = "Arial"
        self.assertTrue(texts.compare_pages(self.data,[self.page]))
    def test_parent_visibility_is_detected(self):
        self.content.visible = False
        self.assertTrue(texts.compare_pages(self.data,[self.page]))
    def test_rasterized_text_is_rejected(self):
        self.layer.kind = "pixel"
        self.assertTrue(texts.compare_pages(self.data,[self.page]))
    def test_manifest_count_and_extra_text_are_detected(self):
        self.assertTrue(texts.compare_pages({"slides":[]},[self.page]))
        self.content.children.append(Layer("legado","Texto legado"))
        self.assertTrue(texts.compare_pages(self.data,[self.page]))
    def test_unicode_utf16_styles(self):
        self.layer = Layer("H1","A😀B")
        self.el["text"] = "A😀B"
        self.assertEqual(texts.compare_style(self.layer,self.el),[])


class ReopenTests(unittest.TestCase):
    def test_hash_and_reexport_pixels_are_bound(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            psd = root/"fixture.psd"
            psd.write_bytes(b"hash fixture")
            proof = root/"pagina_01.png"
            fresh = root/"reopened"
            fresh.mkdir()
            Image.new("RGB",(2,2),"white").save(proof)
            Image.new("RGB",(2,2),"white").save(fresh/proof.name)
            record = registration.record(psd,fresh,"fixture de editor, sem executar aplicativo")
            report = root/"reabertura.json"
            report.write_text(json.dumps(record))
            def verify():
                return texts.verify_reopen(psd,report,[proof],fresh,artifacts.same_rgb,Image.open)
            self.assertEqual(verify(),[])
            psd.write_bytes(b"another PSD revision")
            self.assertTrue(verify())
            record["psd_sha256"] = texts.digest(psd)
            Image.new("RGB",(2,2),"black").save(fresh/proof.name)
            record["pages"][0]["sha256"] = texts.digest(fresh/proof.name)
            report.write_text(json.dumps(record))
            self.assertTrue(verify())


class PackagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
    def put(self,name,value=b"conteudo"):
        p = self.root/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(value)
        return p
    def test_filesystem_excludes_git_credentials_fonts_caches(self):
        for n in [".git/config",".env",".env.local","credentials.json","node_modules/a.js","__pycache__/a.pyc","font.otf","private.pem","dist/old.zip"]:
            self.put(n)
        self.put("documento.md")
        self.assertEqual([p.relative_to(self.root).as_posix() for p in pack.select_files(self.root,True)],["documento.md"])
    def test_git_selection_respects_ignore_and_does_not_include_other_work(self):
        subprocess.run(["git","init","--quiet",str(self.root)],check=True)
        self.put(".gitignore",b"local.log\n")
        self.put("documento.md")
        self.put("local.log")
        self.put(".env")
        subprocess.run(["git","-C",str(self.root),"add","--force",".gitignore","documento.md","local.log",".env"],check=True)
        self.put("em_andamento.md")
        names = {p.name for p in pack.select_files(self.root)}
        self.assertEqual(names,{".gitignore","documento.md"})
    def test_unhydrated_lfs_and_token_are_refused(self):
        for data in [b"version https://git-lfs.github.com/spec/v1\noid sha256:test",("ghp_"+"A"*36).encode()]:
            with self.subTest(data_kind=data[:3]):
                with self.assertRaises(ValueError):
                    pack.check_payload(self.put("asset.txt",data))
    def test_archive_nested_credential_is_refused(self):
        p = self.root/"old.zip"
        with zipfile.ZipFile(p,"w") as archive:
            archive.writestr(".env", "valor")
        with self.assertRaises(ValueError):
            pack.check_payload(p)
    def test_zip_inventory_integrity_and_no_overwrite(self):
        historical = self.put("inventario_sha256.json",b"historico imutavel")
        self.put("documento.md")
        files = pack.select_files(self.root,True)
        inventory = pack.inventory_for(self.root,files)
        output = self.root/"dist"/"pacote.zip"
        sidecar = pack.package(self.root,files,output,inventory)
        self.assertTrue(sidecar.is_file())
        with zipfile.ZipFile(output) as archive:
            self.assertIsNone(archive.testzip())
            report = json.loads(archive.read(self.root.name+"/inventario_publicacao.json"))
            self.assertEqual(report["files"],inventory)
        self.assertEqual(historical.read_bytes(),b"historico imutavel")
        with self.assertRaises(FileExistsError):
            pack.package(self.root,files,output,inventory)
    def test_changed_source_cannot_produce_valid_zip(self):
        path = self.put("a.txt")
        inventory = pack.inventory_for(self.root,[path])
        path.write_bytes(b"mudou depois do inventario")
        output = self.root/"dist"/"invalido.zip"
        with self.assertRaises(RuntimeError):
            pack.package(self.root,[path],output,inventory)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
