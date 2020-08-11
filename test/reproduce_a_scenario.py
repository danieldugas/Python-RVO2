import rvo2
import numpy as np

def reproduce_test_scenario():
    sim = rvo2.PyRVOSimulator(1/60., 1.5, 5, 1.5, 2, 0.4, 2)

    a0 = sim.addAgent((0, 0))
    a1 = sim.addAgent((1, 0))
    a2 = sim.addAgent((1, 1))
    a3 = sim.addAgent((0, 1), 1.5, 5, 1.5, 2, 0.4, 2, (0, 0))

    sim.addObstacle([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1)])
    sim.processObstacles()

    sim.setAgentPrefVelocity(a0, (1, 1))
    sim.setAgentPrefVelocity(a1, (-1, 1))
    sim.setAgentPrefVelocity(a2, (-1, -1))
    sim.setAgentPrefVelocity(a3, (1, -1))

    print('Running simulation')

    positions_log = []
    for step in range(20):
        sim.doStep()

        positions = [sim.getAgentPosition(agent_no) for agent_no in (a0, a1, a2, a3)]
        positions_log.append(positions)

    positions_log = np.array(positions_log)
    # np.savez("positions_log_for_test_scenario.npz", positions_log=positions_log)

    archive = np.load("positions_log_for_test_scenario.npz")

    test_passed = np.allclose(archive['positions_log'], positions_log)

    if test_passed:
        print("Test passed!")
    else:
        print("Test failed!")
    return test_passed


if __name__ == "__main__":
    reproduce_test_scenario()
