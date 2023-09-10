from chanfig import Config, Variable


class BaseConfig(Config):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_file = Variable(str, default="./tests/fasta/single_sequence.fasta")
        self.save_path = Variable(str, default="../results")
        self.auto_fix = Variable(bool, default=False)

        # global parameters
        self.skip_mfe_prediction = Variable(bool, default=False)
        self.skip_dl_prediction = Variable(bool, default=False)
        # self.skip_last_prediction = Variable(bool, default=False)

        # self defined parameters
        self.mse.contrafold.posteriors = 0.0001
