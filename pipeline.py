import kfp
from kfp import dsl

def read_data_op():
    """Read data from the specified source."""
    return dsl.ContainerOp(
        name='Read Data',
        image='us.icr.io/abp-scratchpad/iafai-pipeline-step1:latest',
        command=['sh', '-c'],
        arguments=['python esReading/esDataReader.py'],
        file_outputs={'output': '/iaf/tmp/output'},
        container_kwargs={'working_dir': '/iaf'}
    )


def process_data_op():
    """Preprocess data."""
    return dsl.ContainerOp(
        name='Process Data',
        image='us.icr.io/abp-scratchpad/iafai-pipeline-step1:latest',
        command=['sh', '-c'],
        arguments=['python dataProcessing/dataProcessor.py'],
        file_outputs={'output': '/iaf/tmp/output'},
        container_kwargs={'working_dir': '/iaf'}
    )

def prepare_model_op():
    """Create model and train with training data."""
    return dsl.ContainerOp(
        name='Create and train Model',
        image='us.icr.io/abp-scratchpad/iafai-pipeline-step:latest',
        command=['sh', '-c'],
        arguments=['python modelTraining/trainModel.py'],
        file_outputs={'output': '/iaf/tmp/output'},
        container_kwargs={'working_dir': '/iaf'}
    )

def evaluate_model_op():
    """Store model in specified data store."""
    return dsl.ContainerOp(
        name='Evaluate and store trained Model',
        image='us.icr.io/abp-scratchpad/iafai-pipeline-step:latest',
        command=['sh', '-c'],
        arguments=['python modelEvaluation/testModel.py'],
        file_outputs={'output': '/iaf/tmp/output'},
        container_kwargs={'working_dir': '/iaf'}
    )

def print_op(msg):
    """Print a message."""
    return dsl.ContainerOp(
        name='Print',
        image='us.icr.io/abp-scratchpad/iafai-pipeline-step1:latest',
        command=['echo', msg],
    )
    

@dsl.pipeline(
    name='Anomaly detection model training pipeline',
    description='Shows how to use kubeflow pipelines through IAF.'
)
def pipeline(
    url: str = '',
    token: str = ''
):
    processdata = process_data_op()
    prepare = prepare_model_op()
    evaluate = evaluate_model_op()  
    prepare.after(processdata).set_display_name('Train Model')
    evaluate.after(prepare).set_display_name('Store Model')

if __name__ == '__main__':      
    from kfp_tekton.compiler import TektonCompiler
    TektonCompiler().compile(pipeline, __file__.replace('.py', '.yaml'))
