from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import warnings

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter


logger = logging.getLogger(__name__)

def train_dialogue(domain_file = 'virtual_therapy.yml',
					model_path = './models/dialogue',
					training_data_file = './data/stories.md'):
					
	agent = Agent(domain_file, policies = [MemoizationPolicy(), KerasPolicy()])
	
	agent.train(
				training_data_file,
				max_history = 3,
				epochs = 200,
				batch_size = 50,
				validation_split = 0.2,
				augmentation_factor = 50)
				
	agent.persist(model_path)
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	warnings.filterwarnings("ignore")
	return agent

#print(type(train_dialogue.agent))
	
def run_Chat_bot(serve_forever=True):
	interpreter = RasaNLUInterpreter('./models/nlu/default/therapynlu')
	agent = Agent.load('./models/dialogue', interpreter = interpreter)
	
	if serve_forever:
		agent.handle_channel(ConsoleInputChannel())
		print("Anything")
	warnings.filterwarnings("ignore", category=DeprecationWarning)
	warnings.filterwarnings("ignore")
		
	return agent
	
if __name__ == '__main__':
	train_dialogue()
	run_Chat_bot()


