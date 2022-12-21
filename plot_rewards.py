import pickle   
import numpy as np
import matplotlib.pyplot as plt 

if __name__ == "__main__":

    with open('history/scores_history_SAC42', 'rb') as fp:
        histories = pickle.load(fp)

        print(histories)

    avg_experiments_cumulative_rewards = np.mean(histories, axis=0)
    std_experiments_cumulative_rewards  = np.std(histories , axis=0)

    epochs = np.array(range(len(avg_experiments_cumulative_rewards)))*10
    plt.plot(epochs, avg_experiments_cumulative_rewards, label = "SAC")   
    plt.fill_between(epochs, avg_experiments_cumulative_rewards, 
                            avg_experiments_cumulative_rewards+std_experiments_cumulative_rewards, alpha=0.4)


    plt.xlabel("Épisodes")
    plt.ylabel("Récompenses")

    plt.legend()
    plt.show()