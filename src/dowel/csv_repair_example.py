import sys
sys.path.append(r'src') 

import dowel
from dowel import logger, tabular

logger.add_output(dowel.StdOutput())
logger.add_output(dowel.CsvOutput('out.csv'))
logger.add_output(dowel.TextOutput('out.txt'))
#logger.add_output(dowel.TensorBoardOutput('tensorboard_logdir'))

logger.log('Starting up...')
for i in range(100):
    logger.push_prefix('itr {} '.format(i))
    logger.log('Running training step')

    tabular.record('itr', i)
    tabular.record('loss', 100.0 / (2 + i))

    if i < 50:
        tabular.record('money', 'A')

    if i>10 and i<70:
        tabular.record('luck','B')

    if i > 50:
        tabular.record('new_data', 'C')

    logger.log(tabular)

    tabular.refresh_dict()
    logger.pop_prefix()
    logger.dump_all()

logger.remove_all()
