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
        tabular.record('money', i)

    if i > 50:
        tabular.record('new_data', i)

    if i>10 and i<70:
        tabular.record('luck',i)

    logger.log(tabular)

    tabular.refresh_dict()
    logger.pop_prefix()
    logger.dump_all()

"""If we cannot know all keys name previously, 
we need work again to deal with the "raw" data.

Thus, we should reorganize our file again to achieve desired behaviour 
"""
logger.reorganize_file(tabular,'out.csv')

logger.remove_all()
