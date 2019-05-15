from matplotlib import pyplot as plt
import statistics
import numpy as np

section_map = {
    "Prologo": (-1, 63), "Parodo": (63, 69), "Episodio I": (69, 139), "Stasimo I": (139, 143), "Episodio II": (143, 270),
    "Stasimo II": (270, 274), "Episodio III": (274, 375), "Stasimo III": (375, 377), "Episodio IV": (377, 432),
    "Stasimo IV": (432, 436), "Esodo": (436, 489)
}

# Dark color scheme
color_scheme = {
    "Prologo": ("#000066", ),
    "Parodo": ("black",),
    "Episodio": ("#330066",),
    "Stasimo": ("black",),
    "Esodo": ("#003366",),
    "alpha": 1,
}

# Light color scheme
color_scheme = {
    "Prologo": ("white", ),
    "Parodo": ("red",),
    "Episodio": ("white",),
    "Stasimo": ("red",),
    "Esodo": ("white",),
    "alpha": 0.1,
}

for i, section in enumerate(section_map):
    section_map[section] += color_scheme[section.split()[0]]


# Core averaging functions, lv 1
def mean(sequence):
    sequence = list(filter(None, sequence))

    if len(sequence) > 0:
        return statistics.mean(sequence)
    else:
        return None


def median(sequence):
    sequence = list(filter(None, sequence))
    return statistics.median(sequence)


def maximum(sequence):
    sequence = list(filter(None, sequence))
    return max(sequence)


def minimum(sequence):
    sequence = list(filter(None, sequence))
    return min(sequence)


# Graph averaging functions, lv 2
def continuous_mean(sample_size):
    def mean_func(raw):
        x, y = [], []

        for i in range(len(raw)):

            if i - int(sample_size / 2) > 0 and i + int(sample_size / 2) < len(raw):
                y.append(mean(raw[i - int(sample_size / 2): i + int(sample_size / 2)]))

        x = np.arange(sample_size / 2, len(y) + sample_size / 2)
        return x, y

    return mean_func


def continuous_median(sample_size):
    def median_func(raw):
        x, y = [], []

        for i in range(len(raw)):

            if i - int(sample_size / 2) > 0:
                y.append(median(raw[i - int(sample_size / 2): i + int(sample_size / 2)]))

        x = np.arange(sample_size / 2, len(y) + sample_size / 2)
        return x, y

    return median_func


def exponential_decay(alpha=1, scale_type="approximate", scale_function=maximum):
    def exponential_decay_func(raw):
        x, y = [], []

        for i in range(len(raw)):
            exp_average = 0

            for j in range(len(raw)):
                if raw[j]:
                    if i == j:
                        exp_average += raw[j]
                    else:
                        exp_average += raw[j]/(abs(i-j)**alpha)

            y.append(exp_average)

        y = np.array(y)

        # Scale data
        y *= {
            "approximate": scale_function(raw) / scale_function(y),
            "percentage": 100 / scale_function(y)
        }[scale_type]

        x = np.arange(0, len(y))
        return x, y

    return exponential_decay_func


def direct():
    def direct_func(raw):
        y = raw
        x = np.arange(0, len(y))
        return x, y

    return direct_func


# Optional wrapper functions, lv 3
def derivative(function, n):
    def derivative_func(raw):
        graph = list(function(raw))

        for i in range(n):
            graph[0] = (np.array(graph[0])[:-1] + np.array(graph[0])[1:]) / 2
            graph[1] = np.diff(np.array(graph[1]))

        return graph

    return derivative_func


# Plot graph by running data through outer function, which in turn passes data to inner most function.
# In reality, data is processed from the innermost function to the outermost function.
def build_graph(raw_data, moving_average):

    for character in raw_data:
        graph = np.array(moving_average(raw_data[character]))

        plt.plot(graph[0], graph[1], label=character)


    for section in section_map:
        tpl = section_map[section]
        plt.axvspan(tpl[0], tpl[1], color=tpl[2], alpha=color_scheme["alpha"])
        #plt.text((tpl[0] + tpl[1]) / 2 - len(section) * 4, graph.max() + 0.3, section)

    plt.locator_params(nbins=40)

    plt.xlabel("Strofa")
    plt.ylabel("Parole per strofa")
    plt.legend(loc='upper left')


# multiple build_graph()s can be called before displaying with show_graph()
def show_graph(): plt.show()
