import math
from datatypes import Universe, Body, OrderedPair


# Simulation Code

def simulate_gravity(initial_universe: Universe, num_gens: int, time: float) -> list[Universe]:
    """
    Simulate an N-body system for a fixed number of generations.

    Args:
        initial_universe: The starting state of the universe.
        num_gens: Number of simulation steps to advance (>= 0).
        time: Time step (Δt) between generations (> 0).

    Returns:
        A list of Universe snapshots of length num_gens + 1.
    """
    if not isinstance(initial_universe, Universe):
        raise TypeError("initial_universe must be a Universe")
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer")
    if not isinstance(time, (int, float)) or time <= 0:
        raise ValueError("time must be a positive number")

    time_points: list[Universe] = [initial_universe]

    for i in range(1, num_gens + 1):
        next_universe = update_universe(time_points[i - 1], time)
        time_points.append(next_universe)

    return time_points


def update_universe(current_universe: Universe, time: float) -> Universe:
    """
    Advance the universe by a single time step.

    Computes new accelerations from the current state, then advances velocity and position accordingly.

    Args:
        current_universe: Universe state at the current time.
        time: Time step (Δt) to advance.

    Returns:
        A new Universe instance representing the next state.
    """
    new_universe = copy_universe(current_universe)

    # Update every body in the cloned universe based on forces from current_universe
    for b in new_universe.bodies:
        old_acc, old_vel = b.acceleration, b.velocity
        b.acceleration = update_acceleration(current_universe, b)
        b.velocity = update_velocity(b, old_acc, time)
        b.position = update_position(b, old_acc, old_vel, time)

    return new_universe


def copy_universe(current_universe: Universe) -> Universe:
    """
    Deep-copy a Universe, including all of its bodies.

    Args:
        current_universe: The universe to copy.

    Returns:
        A new Universe with deep-copied bodies and the
        same width and gravitational constant as the original.
    """
    new_bodies: list[Body] = []
    for b in current_universe.bodies:
        new_bodies.append(copy_body(b))

    return Universe(
        new_bodies,
        current_universe.width,
        current_universe.gravitational_constant,
    )


def copy_body(b: Body) -> Body:
    """
    Deep-copy a Body, including its position, velocity, and acceleration.

    Args:
        b: The body to copy.

    Returns:
        A new Body with identical attributes and
        deep-copied OrderedPair objects.
    """
    return Body(
        name=b.name,
        mass=b.mass,
        position=OrderedPair(b.position.x, b.position.y),
        velocity=OrderedPair(b.velocity.x, b.velocity.y),
        acceleration=OrderedPair(b.acceleration.x, b.acceleration.y),
        radius=b.radius,
        red=b.red,
        green=b.green,
        blue=b.blue,
    )


def update_acceleration(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute a body's acceleration from the net gravitational force.

    Args:
        current_universe: The universe containing all bodies.
        b: The body whose acceleration is being computed.

    Returns:
        An OrderedPair (ax, ay) representing the updated acceleration.
    """
    net_force = compute_net_force(current_universe, b)

    # apply Newton's second law over components
    ax = net_force.x / b.mass
    ay = net_force.y / b.mass

    return OrderedPair(ax, ay)


def compute_net_force(current_universe: Universe, b: Body) -> OrderedPair:
    """
    Compute the net gravitational force on a body from all other bodies.

    Args:
        current_universe: The universe containing all bodies.
        b: The body on which the net force is computed.

    Returns:
        An OrderedPair (Fx, Fy) representing the net gravitational force.
    """
    net_force = OrderedPair(0.0, 0.0)
    G = current_universe.gravitational_constant

    # range over bodies and determine force acting on b
    for cur_body in current_universe.bodies:
        if cur_body is not b:
            current_force = compute_force(b, cur_body, G)
            net_force.x += current_force.x
            net_force.y += current_force.y

    return net_force


def compute_force(b1: Body, b2: Body, G: float) -> OrderedPair:
    """
    Compute the gravitational force exerted on b1 by b2.

    Args:
        b1: The body on which the force is acting.
        b2: The body exerting the gravitational force.
        G: Gravitational constant.

    Returns:
        An OrderedPair (Fx, Fy) representing the force on b1.
    """
    d = distance(b1.position, b2.position)
    if d == 0.0:
        return OrderedPair(0.0, 0.0)  # treat as no force

    F_magnitude = G * b1.mass * b2.mass / (d * d)

    # break F into components
    dx = b2.position.x - b1.position.x
    dy = b2.position.y - b1.position.y
    Fx = F_magnitude * dx / d
    Fy = F_magnitude * dy / d

    return OrderedPair(Fx, Fy)


def distance(p1: OrderedPair, p2: OrderedPair) -> float:
    """
    Compute the Euclidean distance between two position vectors.

    Args:
        p1: The first position vector.
        p2: The second position vector.

    Returns:
        The distance between p1 and p2.
    """
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx * dx + dy * dy)


def update_velocity(b: Body, old_acceleration: OrderedPair, time: float) -> OrderedPair:
    """
    Update velocity using average acceleration over the step.

    Formula:
        v_{t+Δt} = v_t + 0.5 * (a_t + a_{t+Δt}) * Δt

    Args:
        b: The body whose velocity is being updated.
        old_acceleration: The acceleration at the previous time step.
        time: The time step Δt.

    Returns:
        An OrderedPair containing the updated velocity (vx, vy).
    """
    vx = b.velocity.x + 0.5 * (b.acceleration.x + old_acceleration.x) * time
    vy = b.velocity.y + 0.5 * (b.acceleration.y + old_acceleration.y) * time
    return OrderedPair(vx, vy)


def update_position(b: Body, old_acc: OrderedPair, old_vel: OrderedPair, time: float) -> OrderedPair:
    """
    Update position using constant-acceleration kinematics.

    Formula:
        p_{t+Δt} = p_t + v_t * Δt + 0.5 * a_t * Δt²

    Args:
        b: The body whose position is being updated.
        old_acc: The acceleration at the previous time step.
        old_vel: The velocity at the previous time step.
        time: The time step Δt.

    Returns:
        An OrderedPair containing the updated position (px, py).
    """
    px = b.position.x + old_vel.x * time + 0.5 * old_acc.x * time * time
    py = b.position.y + old_vel.y * time + 0.5 * old_acc.y * time * time
    return OrderedPair(px, py)
