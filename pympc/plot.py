# external imports
import numpy as np
import matplotlib.pyplot as plt

def plot_state_space_trajectory(x, dim=[0,1], text=False, label=None, **kwargs):
    """
    Plots one component of the state x as a function of another (2d plot).

    Arguments
    ----------
    x : list of numpy.ndarray
        Trajectory of the state.
    dim : list of int
        List of the indices of the components of the state that we want to plot (2 indices).
    """

    # check inputs
    if len(dim) != 2:
        raise ValueError('can plot only 2-dimensional trajectories.')

    # plot trajectory
    for t in range(len(x)-1):
        if t == 0:
            plt.plot(
                [x[0][dim[0]], x[1][dim[0]]],
                [x[0][dim[1]], x[1][dim[1]]],
                label=label,
                **kwargs
                )
        plt.plot(
            [x[t][dim[0]], x[t+1][dim[0]]],
            [x[t][dim[1]], x[t+1][dim[1]]],
            **kwargs
            )

    # plot text
    for t in range(len(x)):
        if text:
            plt.text(x[t][0], x[t][1], r'$x('+str(t)+')$')

    # scatter initial condition
    plt.scatter(
        x[0][dim[0]],
        x[0][dim[1]],
        color='w',
        edgecolor='k',
        zorder=3
        )

    # axis labels
    plt.xlabel(r'$x_{' + str(dim[0]+1) + '}$')
    plt.ylabel(r'$x_{' + str(dim[1]+1) + '}$')

def plot_input_sequence(u, h, u_bounds=None):
    """
    Plots the input sequence and its bounds as functions of time.

    Arguments
    ----------
    u : list of numpy.ndarray
        Sequence of the input vectors.
    h : float
        Time step.
    u_bounds : list of numpy.ndarray
        Lower and upper bound on the control action.
    """

    # dimension of the input
    nu = u[0].shape[0]

    # time axis
    N = len(u)
    t = np.linspace(0, N*h, N+1)

    # plot each input element separately
    for i in range(nu):
        plt.subplot(nu, 1, i+1)

        # plot input sequence
        u_i_sequence = [u[k][i] for k in range(N)]
        input_plot, = plt.step(t, [u_i_sequence[0]] + u_i_sequence, 'b')

        # plot bounds if provided
        if u_bounds is not None:
            for bound in u_bounds:
                bound_plot, = plt.step(t, bound[i]*np.ones(t.shape), 'r')

        # miscellaneous
        plt.ylabel(r'$u_{' + str(i+1) + '}$')
        plt.xlim((0., N*h))
        if i == 0:
            if u_bounds is not None:
                plt.legend(
                    [input_plot, bound_plot],
                    ['Optimal control', 'Control bounds'],
                    loc=1
                    )
            else:
                plt.legend(
                    [input_plot],
                    ['Optimal control'],
                    loc=1
                    )
    plt.xlabel(r'$t$')

def plot_state_trajectory(x, h, x_bounds=None):
    """
    Plots the state trajectory and its bounds as functions of time.

    Arguments
    ----------
    x : list of numpy.ndarray
        Sequence of the state vectors.
    h : float
        Time step.
    x_bounds : list of numpy.ndarray
        Lower and upper bound on the state.
    """

    # dimension of the state
    nx = x[0].shape[0]

    # time axis
    N = len(x) - 1
    t = np.linspace(0, N*h, N+1)

    # plot each state element separately
    for i in range(nx):
        plt.subplot(nx, 1, i+1)

        # plot state trajectory
        x_i_trajectory = [x[k][i] for k in range(N+1)]
        state_plot, = plt.plot(t, x_i_trajectory, 'b')

        # plot bounds if provided
        if x_bounds is not None:
            for bound in x_bounds:
                bound_plot, = plt.step(t, bound[i]*np.ones(t.shape),'r')

        # miscellaneous
        plt.ylabel(r'$x_{' + str(i+1) + '}$')
        plt.xlim((0., N*h))
        if i == 0:
            if x_bounds is not None:
                plt.legend(
                    [state_plot, bound_plot],
                    ['Optimal trajectory', 'State bounds'],
                    loc=1
                    )
            else:
                plt.legend(
                    [state_plot],
                    ['Optimal trajectory'],
                    loc=1
                    )
    plt.xlabel(r'$t$')

def plot_output_trajectory(C, x, h, y_bounds=None):
    """
    Plots the output trajectory and its bounds as functions of time.

    Arguments
    ----------
    C : numpy.ndarray
        Tranformation matrix between the state and the output.
    x : list of numpy.ndarray
        Sequence of the state vectors.
    h : float
        Time step.
    y_bounds : list of numpy.ndarray
        Lower and upper bound on the output.
    """

    # apply linear transformation
    y = [C.dot(x_t) for x_t in x]

    # number of plots
    ny = C.shape[0]

    # time axis
    N = len(x) - 1
    t = np.linspace(0, N*h, N+1)

    # plot each state element separately
    for i in range(ny):
        plt.subplot(ny, 1, i+1)

        # plot state trajectory
        y_i_trajectory = [y[k][i] for k in range(N+1)]
        output_plot, = plt.plot(t, y_i_trajectory, 'b')

        # plot bounds if provided
        if y_bounds is not None:
            for bound in y_bounds:
                bound_plot, = plt.step(t, bound[i]*np.ones(t.shape),'r')

        # miscellaneous options
        plt.ylabel(r'$y_{' + str(i+1) + '}$')
        plt.xlim((0., N*h))
        if i == 0:
            if y_bounds is not None:
                plt.legend(
                    [output_plot, bound_plot],
                    ['Optimal trajectory', 'Output bounds'],
                    loc=1
                    )
            else:
                plt.legend(
                    [output_plot],
                    ['Optimal trajectory'],
                    loc=1
                    )
    plt.xlabel(r'$t$')


def plot_partition_explicit_solution(explicit_solution, print_active_set=False, **kwargs):
    """
    Plots the state partition for the 2d solution of an explicit mpc problem.

    Arguments
    ----------
    explicit_solution : instance of ExplicitSolution
        Solution of a multiparametric quadratic program.
    print_active_set : bool
        If True it prints the active set of each critical region in its center.
    """

    # check that the required plot is 2d
    if explicit_solution.critical_regions[0].polyhedron.A.shape[1] != 2:
        raise ValueError('can plot only 2-dimensional partitions.')

    # plot every critical region with random colors
    for cr in explicit_solution.critical_regions:
        cr.polyhedron.plot(facecolor=np.random.rand(3), **kwargs)

        # if required print active sets
        if print_active_set:
            plt.text(cr.polyhedron.center[0], cr.polyhedron.center[1], str(cr.active_set))

def plot_value_function_mpqp(mpqp, explicit_solution, resolution=100, **kwargs):
    """
    Plots the level sets of the optimal value function V*(x) of the explicit solution of an mpc problem.

    Arguments
    ----------
    mpqp : instance of MultiParametricQuadraticProgram
        Multiparametric quadratic program of which we want to plot the optimal value function.
    explicit_solution : instance of ExplicitSolution
        Solution of a multiparametric quadratic program.
    resolution : float
        Size of the grid for the contour plot.
    """

    # check dimension of the state
    if explicit_solution.critical_regions[0].polyhedron.A.shape[1] != 2:
        raise ValueError('can plot only 2-dimensional partitions.')

    # get feasible set
    feasible_set = mpqp.get_feasible_set()

    # create box containing the feasible set
    x_max = max([v[0] for v in feasible_set.vertices])
    x_min = min([v[0] for v in feasible_set.vertices])
    y_max = max([v[1] for v in feasible_set.vertices])
    y_min = min([v[1] for v in feasible_set.vertices])

    # create grid
    x = np.linspace(x_min, x_max, resolution)
    y = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x, y)

    # evaluate grid
    zs = np.array([explicit_solution.V(np.array([x,y])) for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)

    # plot
    feasible_set.plot(**kwargs)
    cp = plt.contour(X, Y, Z)
    plt.colorbar(cp)
    plt.title(r'$V^*(x)$')