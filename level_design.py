from pgzero.builtins import Actor
from utils import ActorContainer
import csv

class Level(ActorContainer):
    def place_block(self, block):
        self.actor_list.append(block)
    
    def save_file(self, file):
        with open(file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['image', 'x', 'y'], dialect='unix')
            writer.writeheader()
            
            for element in self.actor_list:
                writer.writerow({
                    'image': element.image, 
                    'x': element.x, 
                    'y': element.y
                })
    
    def read_file(self, file):
        with open(file, 'r') as f:
            reader = csv.DictReader(f, dialect='unix')
            for row in reader:
                if not row:
                    break

                self.place_block(Actor(row['image'], pos=(float(row['x']), float(row['y']))))
                