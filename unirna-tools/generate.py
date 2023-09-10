import subprocess
from multiprocessing import Pool
from typing import Any

from .config import BaseConfig
from .conversion import fasta_extraction


class mse_engine:
    def __init__(self, config) -> None:
        super().__init__(config)
        self.sanity, self.ids, self.seqs = fasta_extraction(self.config.input_fasta, auto_fix=self.auto_fix)
        if not self.sanity:
            raise ValueError("Fasta file is not valid")

    def run_command(self, engine, args=(), stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        proc = subprocess.run(engine, capture_output=True, stdout=stdout, stderr=stderr, *args)
        return proc.stdout, proc.stderr

    def run_contrafold(self):
        if len(self.ids) == 1:
            args_list = ["prediction", self.config.input_fasta, "--posteriors", self.config.posteriors_cutoff]
        else:
            args_list = [
                "prediction",
                self.config.input_fasta,
                "--posteriors",
                self.config.posteriors_cutoff,
                "--batch",
            ]


class dl_engine:
    def __init__(self, config) -> None:
        super().__init__(config)


class main_engine:
    def __init__(self, config) -> None:
        super().__init__(config)
        self.classes = []
        self.results = []

    def register_engine(self, cls):
        self.classes.append(cls)

    def run(self):
        for cls in self.classes:
            cls.run()


if __name__ == "__main__":
    config = BaseConfig()
    config = config.parse(default_config="config", no_default_config_action="warn")  # type: ignore
    runner = main_engine(config)

    if not config.get("skip_mfe_prediction", False):
        runner.register_engine(mse_engine(config))
        print("Skipping MFE prediction")

    if not config.get("skip_dl_prediction", False):
        runner.register_engine(dl_engine(config))
        print("Skipping DL prediction")
