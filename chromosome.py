import heapq
import matplotlib.pyplot as plt
import random


class Chromosome:
    """"
    Represents a chromosome in a genetic algorithm.
    Attributes:
        shape_order (list): A list representing the order of shapes in the chromosome.
        rotations (list): A list representing the rotation angles for each shape.
        fitness (float): The fitness value of the chromosome, initialized to None.
    """

    def __init__(self, shape_order, rotations, dimensions, paper_width, paper_height):
        """
        Initializes a Chromosome instance.
        Args:
            shape_order (list[int]): A list representing the order of shapes.
            rotations (list[boolean]): A list representing the rotation angles for each shape.
        """
        assert len(shape_order) == len(rotations), "Shape order and rotations must have the same length."
        self.shape_order = shape_order
        self.rotations = rotations
        self.fitness = self.calculate_fitness(paper_width, paper_height ,dimensions)

    
    def __str__(self):
        return f"Chromosome with shape order: {self.shape_order} and rotations: {self.rotations}"
    
    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False
        return (self.shape_order == other.shape_order and
                self.rotations == other.rotations)
    
    def __len__(self):
        return len(self.shape_order)

    def _rectangles_overlap(self, r1, r2):
        return not (r1['x'] + r1['width'] <= r2['x'] or
                    r2['x'] + r2['width'] <= r1['x'] or
                    r1['y'] + r1['height'] <= r2['y'] or
                    r2['y'] + r2['height'] <= r1['y'])
    
    def bottom_left_with_heap(self, paper_width, paper_height, dimensions):
        """
        Bottom-left packing algorithm using a min-heap to efficiently find the next available position.
        Args:
            paper_width (int): Width of the paper.
            paper_height (int): Height of the paper.
            dimensions (list[dict[]]): List of rectangles to be placed, each represented as a dictionary with 'width', 'height' and 'number' keys.
        """
        placed = []
        active_points = []
        heapq.heappush(active_points, (0, 0))

        for idx, shape in enumerate(self.shape_order):
            found_pos = None
            rect_width = dimensions[shape]['width']
            rect_height = dimensions[shape]['height']
            if self.rotations[idx]:
                # Swap width and height if the shape is rotated
                rect_width, rect_height = rect_height, rect_width

            while active_points:
                y, x = heapq.heappop(active_points)
                # Check if the rectangle fits within the paper dimensions
                if x + rect_width > paper_width or y + rect_height > paper_height:
                    continue

                # Check for overlap with already placed rectangles
                new_rect = {'x': x, 'y': y, 'width': rect_width, 'height': rect_height}
                overlap = any(self._rectangles_overlap(new_rect, r) for r in placed)

                if not overlap:
                    found_pos = (x, y)
                    break

            if found_pos:
                x, y = found_pos
                placed.append({'x': x, 'y': y, 'width': rect_width, 'height': rect_height, 'shape': shape})

                # Add new active points to the heap
                heapq.heappush(active_points, (y, x + rect_width))
                heapq.heappush(active_points, (y + rect_height, x))
            else:
                # If no position was found, we skip placing this rectangle
                # !!! Get back to this later, maybe throw an error or handle it differently !!!
                pass

        return placed

    def calculate_fitness(self, paper_width, paper_height, dimensions):
        """
        Calculate the fitness of the chromosome.
        Args:
            paper_width (float): The width of the paper.
            paper_height (float): The height of the paper.
            placed_rectangles (list[dict]): List of rectangles placed by the bottom-left algorithm.
        Returns:
            float: The fitness value of the chromosome (lower is better).
        """
        placed_rectangles = self.bottom_left_with_heap(paper_width, paper_height, dimensions)
        if not placed_rectangles:
            return float('inf')  # If no rectangles were placed, return infinite fitness

        total_area = sum(r['width'] * r['height'] for r in placed_rectangles)

        max_rect_dimension = max(max(r['width'], r['height']) for r in placed_rectangles)
        # Used paper height
        max_y = max(r['y'] + r['height'] for r in placed_rectangles)
        fitness = max_y
        # used_paper_area = paper_width * max_y

        if len(placed_rectangles) < len(self.shape_order):
            # If not all rectangles were placed, we consider the fitness to be lower
            fitness = max_y + (len(self.shape_order) - len(placed_rectangles)) * max_rect_dimension  # Penalize for unplaced rectangles

        return fitness
    
    def show(self, paper_width, paper_height, dimensions):
        """
        Visualizes the chromosome by plotting the rectangles on a paper.
        Args:
            paper_width (int): Width of the paper.
            paper_height (int): Height of the paper.
            dimensions (list[dict]): List of rectangles to be placed, each represented as a dictionary with 'width', 'height' and 'number' keys.
        """

        placed_rectangles = self.bottom_left_with_heap(paper_width, paper_height, dimensions)

        fig, ax = plt.subplots()
        ax.set_xlim(0, paper_width)
        ax.set_ylim(0, paper_height)
        ax.set_aspect('equal')
        
        # colors = plt.cm.get_cmap('tab20', len(dimensions))
        colors = [plt.cm.viridis(i / len(dimensions)) for i in range(len(dimensions))]


        for rect in placed_rectangles:
            color = colors[rect['shape']]
            ax.add_patch(plt.Rectangle((rect['x'], rect['y']), rect['width'], rect['height'], fill=True, facecolor=color, edgecolor='black'))

        plt.title(f"Chromosome Fitness: {self.fitness:.2f}")
        plt.show()
    

if __name__ == '__main__':
    # Test the Chromosome class
    shape_order = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    rotations = [False, True, False, False, True, False, True, False, True]
    dimensions = [
        {'width': 100, 'height': 50},
        {'width': 60, 'height': 80},
        {'width': 30, 'height': 40},
    ]
    paper_width = 500
    paper_height = 500

    chromosome = Chromosome(shape_order, rotations, dimensions, paper_width, paper_height)
    chromosome.show(paper_width, paper_height, dimensions)
    

