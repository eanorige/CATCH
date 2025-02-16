# =======================================================================
# Copyright 2025 UCLA NanoCAD Laboratory
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =======================================================================

import matplotlib.pyplot as plt
import math
import sys

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Extract x-axis and y-axis
    x_axis_label = lines[0].strip().split(':')[1].strip()
    y_axis_label = lines[1].strip().split(':')[1].strip()

    # Extract x-labels from line 2 starting after the ":"
    x_labels = lines[2].strip().split(':')[1].strip().split()
    #x_labels = lines[2].strip().split()[1:]

    y_values = []
    series_labels = []

    stack = False

    # Extract the numbers from the subsequent lines
    if lines[3].strip().split()[0] == 'series:':
        lines_per_series = len(x_labels) + 1
        for series in range(0, (len(lines) - 3) // lines_per_series):
            series_labels.append(lines[3 + series * lines_per_series].strip().split(':')[1].strip())
            sub_list = []
            for line in lines[lines_per_series * series + 4:lines_per_series * (series + 1) + 4 - 1]:
                sub_str_list = line.strip().split()
                sub_list.append([float(value) for value in sub_str_list])
                #sub_list.append([float(value) for value in line.strip().split()])
            y_values.append(sub_list)
    elif lines[3].strip().split()[0] == 'stack:':
        # series_labels should be interpreted as the labels for the different segments of the stacked bar chart here.
        series_labels = lines[3].strip().split(':')[1].strip().split()
        intermediate_y_values = []
        lines_per_series = len(x_labels)
        for line in lines[4:lines_per_series + 4]:
            sub_list = []
            for value in line.strip().split():
                sub_list.append(float(value))
            intermediate_y_values.append(sub_list)
        for i in range(len(intermediate_y_values[0])):
            y_values.append([intermediate_y_values[j][i] for j in range(len(intermediate_y_values))])
        stack = True
    else:
        series_labels.append("")
        series = [float(line.strip()) for line in lines[3:]]
        y_values.append(series)

    return x_axis_label, y_axis_label, x_labels, y_values, series_labels, stack

def plot_data(x_axis_label, y_axis_label, x_labels, y_values, series_labels, stack, rotation, plot_type, output_filename, x_justification='right'):
    plt.figure(figsize=(10, 6))

    bar_width = 0.5

    if stack:
        for i in range(len(y_values)):
            sum_y_values = []
            for j in range(len(y_values[i])):
                sum_y_values.append(sum([y_values[k][j] for k in range(i)]))
            plt.bar(x_labels, y_values[i], label=series_labels[i], bottom=sum_y_values, width=bar_width)
        plt.legend()
    else:
        if plot_type == 'line':
            if len(series_labels) > 1:
                for i in range(len(y_values)):
                    plt.plot(x_labels, y_values[i], marker='o', label=series_labels[i])
                plt.legend()
            else:
                plt.plot(x_labels, y_values[0], marker='o')
        elif plot_type == 'bar':
            if len(series_labels) > 1:
                for i in range(len(y_values)):
                    plt.bar(x_labels, y_values[i], label=series_labels[i], width=bar_width)
                plt.legend()
            else:
                plt.bar(x_labels, y_values[0], width=bar_width)
        else:
            print("Invalid plot type. Use 'line' or 'bar'.")
            return

    fontsize=22

    plt.xlabel(x_axis_label, fontsize=fontsize)
    plt.ylabel(y_axis_label, fontsize=fontsize)
    # plt.title(f'{x_axis_label} vs {y_axis_label}', fontsize=fontsize)
    if len(series_labels) > 1:
        # Count up the total number of characters in the series labels
        total_chars = sum([len(label) for label in series_labels])
        n_cols = math.ceil(len(series_labels)/math.ceil(total_chars/20))
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=fontsize-10, ncol=n_cols)
    plt.grid(True)
    plt.xticks(rotation=rotation, ha=x_justification, fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    # Output to file
    plt.savefig(output_filename)
    # Display the plot
    # plt.show()

def main():
    if len(sys.argv) != 6:
        print("Usage: python generate_plot.py <input_file> <rotation> <x_justification> <plot_type> <output_file>")
        sys.exit(1)

    filename = sys.argv[1]
    rotation = float(sys.argv[2])
    x_justification = sys.argv[3]
    plot_type = sys.argv[4]
    output_filename = sys.argv[5]
    x_axis_label, y_axis_label, x_labels, y_values, series_labels, stack = read_data(filename)
    plot_data(x_axis_label, y_axis_label, x_labels, y_values, series_labels, stack, rotation, plot_type, output_filename, x_justification)

if __name__ == "__main__":
    main()
