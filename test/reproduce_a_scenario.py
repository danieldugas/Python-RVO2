import rvo2
import numpy as np

def reproduce_test_scenario(plotting=False):
    sim = rvo2.PyRVOSimulator(1/60., 1.5, 5, 1.5, 2, 0.4, 2)

    a0 = sim.addAgent((-1, -1))
    a1 = sim.addAgent((1, -1))
    a2 = sim.addAgent((1, 1))
    a3 = sim.addAgent((-1, 1), 1.5, 5, 1.5, 2, 0.4, 2, (0, 0))

    obstacles = [
        [(0.3, 0.1), (0.1, 0.1), (0.1, -0.1)]
    ]
    for obstacle in obstacles:
        sim.addObstacle(obstacle)
    sim.processObstacles()

    sim.setAgentPrefVelocity(a0, (1, 1))
    sim.setAgentPrefVelocity(a1, (-1, 1))
    sim.setAgentPrefVelocity(a2, (-1, -1))
    sim.setAgentPrefVelocity(a3, (1, -1))

    print('Running simulation')

    positions_log = []
    for step in range(200):
        sim.doStep()

        positions = [sim.getAgentPosition(agent_no) for agent_no in (a0, a1, a2, a3)]
        positions_log.append(positions)

    positions_log = np.array(positions_log)
#     np.savez("positions_log_for_test_scenario.npz",
#              positions_log=positions_log,
#              obstacles=np.array(obstacles))

    archive = np.load("positions_log_for_test_scenario.npz")

    test_passed = np.allclose(archive['positions_log'], positions_log)

    if plotting:
        plot_obstacles(np.array(obstacles))
        plot_positions_log(positions_log)
        plot_positions_log(archive['positions_log'])

    if test_passed:
        print("Test passed!")
    else:
        print("Test failed!")
    return test_passed

def plot_positions_log(positions_log):
    n_traj = positions_log.shape[1]
    for i in range(n_traj):
        plt.plot(positions_log[:,i,0], positions_log[:,i,1])

def plot_obstacles(obstacles):
    for obstacle in obstacles:
        c = np.concatenate([obstacle, obstacle[:1]], axis=0)
        plt.plot(c[:,0], c[:,1], 'k')


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    reproduce_test_scenario(plotting=True)
    plt.show()
