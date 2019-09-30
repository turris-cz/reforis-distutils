import copy
import os
import pathlib
import re
from distutils.cmd import Command

from setuptools.command.build_py import build_py


class ForisBuild(Command):
    def run(self, path):
        build_py.run(self)
        self.npm_install_and_build(path)
        self.copy_translations_from_forisjs(path)
        self.compile_translations(path)

    def npm_install_and_build(self, path):
        os.system(f'cd {path}/js; npm install --save-dev')
        build_dir = path / self.build_lib / 'reforis_static/reforis/js'
        os.system(f'cd {path}/js; npm run-script build -- -o {build_dir}/app.min.js')

    def copy_translations_from_forisjs(self, path):
        for po in path.glob('js/node_modules/foris/translations/*/LC_MESSAGES/forisjs.po'):
            lang = pathlib.Path(po).parent.parent.name
            path_to_copy = path / f'reforis/translations/{lang}/LC_MESSAGES/forisjs.po'
            os.system(f'cp {po} {path_to_copy}')

    def compile_translations(self, path):
        def compile_language(domain, path):
            from babel.messages import frontend as babel
            distribution = copy.copy(self.distribution)
            cmd = babel.compile_catalog(distribution)
            cmd.input_file = str(path)
            lang = re.match(r".*/reforis/translations/([^/]+)/LC_MESSAGES/.*po", str(path)).group(1)
            out_path = BASE_DIR / self.build_lib / f"reforis/translations/{lang}/LC_MESSAGES/{domain}.mo"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            cmd.output_file = str(out_path)
            cmd.domain = domain
            cmd.ensure_finalized()
            cmd.run()

        def compile_domain(domain):
            for path in BASE_DIR.glob(f'reforis/translations/*/LC_MESSAGES/{domain}.po'):
                compile_language(domain, path)

        compile_domain('messages')
        compile_domain('tzinfo')
        compile_domain('forisjs')
