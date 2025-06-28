import heapq


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
            shape_order (list): A list representing the order of shapes.
            rotations (list): A list representing the rotation angles for each shape.
        """
        self.shape_order = shape_order
        self.rotations = rotations
        self.fitness = self._calculate_fitness(paper_width, paper_height ,dimensions)


    def __repr__(self):
        return f"Chromosome(genes={self.genes})"
    
    def __str__(self):
        return f"Chromosome with shape order: {self.shape_order} and rotations: {self.rotations}"
    
    def __eq__(self, other):
        """Check if two chromosomes are equal based on their shape order and rotations."""
        if not isinstance(other, Chromosome):
            return False
        return (self.shape_order == other.shape_order and
                self.rotations == other.rotations)
    

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
            given_rectangles (list[dict[]]): List of rectangles to be placed, each represented as a dictionary with 'width', 'height' and 'number' keys.
        """
        placed = []
        active_points = []
        heapq.heappush(active_points, (0, 0))

        for i in self.shape_order:
            found_pos = None
            rect_width = dimensions[i]['width']
            rect_height = dimensions[i]['height']
            if self.rotations[i]:
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
                placed.append({'x': x, 'y': y, 'width': rect_width, 'height': rect_height})

                # Add new active points to the heap
                heapq.heappush(active_points, (y, x + rect_width))
                heapq.heappush(active_points, (y + rect_height, x))
            else:
                # If no position was found, we skip placing this rectangle
                # !!! Get back to this later, maybe throw an error or handle it differently !!!
                pass

        return placed

    def _calculate_fitness(self, paper_width, paper_height, dimensions):
        """
        Calculate the fitness of the chromosome.
        Args:
            paper_width (float): The width of the paper.
            paper_height (float): The height of the paper.
            placed_rectangles (list[dict]): List of rectangles placed by the bottom-left algorithm.
        """
        placed_rectangles = self.bottom_left_with_heap(paper_width, paper_height, dimensions)
        if not placed_rectangles:
            return 0.0

        total_area = sum(r['width'] * r['height'] for r in placed_rectangles)

        # Used paper height
        max_y = max(r['y'] + r['height'] for r in placed_rectangles)

        used_paper_area = paper_width * max_y

        if used_paper_area > paper_width * paper_height:
            # used_paper_area = paper_width * paper_height
            pass # !!! Get back to this later, maybe throw an error or handle it differently !!!

        fitness = total_area / used_paper_area

        return fitness

        
    def encode(self):
        """Encode the chromosome's genes into a binary representation."""
        pass
        
