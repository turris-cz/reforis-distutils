import copy
import os
import pathlib
import re
from distutils.cmd import Command


class BaseForisBuild(Command):
    def npm_install_and_build(self, path, module_name):
        os.system(f'cd {path}/js; npm install --save-dev')
        build_dir = path / self.build_lib / 'reforis_static' / module_name / 'js'
        os.system(f'cd {path}/js; npm run-script build -- -o {build_dir}/app.min.js')

    def compile_translations(self, path, module_name, domains):
        def compile_language(domain, trans_path):
            from babel.messages import frontend as babel
            distribution = copy.copy(self.distribution)
            cmd = babel.compile_catalog(distribution)
            cmd.input_file = str(trans_path)
            lang = re.match(f'.*/{module_name}/translations/([^/]+)/LC_MESSAGES/.*po', str(trans_path)).group(1)
            out_path = path / self.build_lib / f"{module_name}/translations/{lang}/LC_MESSAGES/{domain}.mo"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            cmd.output_file = str(out_path)
            cmd.domain = domain
            cmd.ensure_finalized()
            cmd.run()

        def compile_domain(domain):
            for trans_path in path.glob(f'{module_name}/translations/*/LC_MESSAGES/{domain}.po'):
                compile_language(domain, trans_path)

        for domain in domains:
            compile_domain(domain)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class ForisBuild(BaseForisBuild):
    def run(self):
        self.npm_install_and_build(path=self.root_path, module_name='reforis')
        self.copy_translations_from_forisjs(path=self.root_path)
        self.compile_translations(path=self.root_path, module_name='reforis', domains=('messages', 'tzinfo', 'forisjs'))

    def copy_translations_from_forisjs(self, path):
        for po in path.glob('js/node_modules/foris/translations/*/LC_MESSAGES/forisjs.po'):
            lang = pathlib.Path(po).parent.parent.name
            path_to_copy = path / f'reforis/translations/{lang}/LC_MESSAGES/forisjs.po'
            os.system(f'cp {po} {path_to_copy}')


class ForisPluginBuild(BaseForisBuild):
    def run(self):
        self.npm_install_and_build(path=self.root_path, module_name=self.module_name)
        self.compile_translations(path=self.root_path, module_name=self.module_name, domains=('messages',))
