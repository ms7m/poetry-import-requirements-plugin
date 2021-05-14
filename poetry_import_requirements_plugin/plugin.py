from cleo.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option
from poetry.poetry import Poetry

import rparse
import pathlib

import typing

class ImportExternalRequirements(Command):
    name = "install-from-requirements"
    arguments = [
        Argument(
            name="file",
            required=True,
            description="A direct path to the requirements.txt file."
        ),
    ]
    options = [
        
        Option(
            name="requirements-file",
            shortcut="-r",
            description="set file as an requirements.txt"
        ),
        Option(
            name="pipfile",
            shortcut="-p",
            description="set file as an Pipfile.lock"
        ),
        Option(
            name="conda",
            shortcut="-c",
            description="set file as an conda.yml"
        ),
        Option(
            name="tox",
            shortcut="-t",
            description="set file as an tox",
        ),
        
        # Optioanl
        Option(
            name="dry-run",
            shortcut="-D",
            description="If enabled, this will NOT install any packages, and will simply display the poetry command to install",
        )
    ]
    def handle(self):
        settings = {
            "path": self.argument("file"),
        }
        
        
        absolute_path_to_file = pathlib.Path(settings['path']).absolute()
        if absolute_path_to_file.exists() == False:
            self.line_error(f"File path {absolute_path_to_file} does not exist.")
            return 1
        
        try:
            parse_requirements_file = rparse.parse(open(absolute_path_to_file, 'r').read()) # type: typing.List[rparse.Requirement]
        except Exception as error:
            self.line_error(f"Requirements file is malformed: {error}")
        
        
        for requirement in parse_requirements_file:
            if len(requirement.specs) > 1:
                generated_version = "".join(requirement.specs[0])
                for req in requirement.specs[1:]:
                    generated_version += f",{''.join(req)}"
            else:
                generated_version = "".join(requirement.specs[0])
            
            generated_command = f"poetry install {requirement.name}{generated_version}"    
            if self.option("dry-run") == False:
                self.call("install", f"{requirement.name}{generated_version}")
            else:
                self.line(f"<b>{generated_command}</b>")
                

def factory():
    return ImportExternalRequirements()


class MyApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory(ImportExternalRequirements.name, factory)
        