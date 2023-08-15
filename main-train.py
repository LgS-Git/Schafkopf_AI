from NEAT.network import eval_genomes, save_genomes
import neat

# Load NEAT configuration
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'NEAT/neat_config.txt')

# Create the population
p = neat.Population(config)

# Add reporters for stats
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

# Run NEAT
winner = p.run(eval_genomes, 3)

save_genomes(winner, 'NEAT/genomes/winner.pkl')
save_genomes(p, 'NEAT/genomes/fittest_pop.pkl')
