"""
@author Gabriela Melo
@since 21/05/2015
"""

class MinHeap:
	def __init__(self):
		self.count = 0
		self.array = [None]

	def __len__(self):
		return self.count

	def is_empty(self):
		'''
        returns whether the amount of items in the heap is 0
        :return: boolean
        :complexity: O(1)
        '''
		return self.count == 0

	def append(self, item):
		'''
        adds a new item to the heap
        :param item: a list of any object type, except for item[0] which contains the key, that must be an integer
        :complexity: best = O(1), worst = O(log N), where N = depth of heap
        '''
		try:
			int(item[0])
		except ValueError:
			print('Key needs to be an integer')
		try:
			self.array[self.count+1] = item
		except IndexError:
			self.array.append(item)

		self.count += 1
		self.rise(self.count)

	def appendAtEnd(self, value):
		self.array.append[self.count+1] = [self.array[self.count][0]+1, value]


	def rise(self, k):
		'''
		brings item of key k to the position where it belongs
		:param k: integer, position of item
		:complexity: best = O(1), worst = O(log k)
		'''
		while k//2 > 0:
			if self.array[k][0] >= self.array[k//2][0]:
				break
			self.swap(k, k//2)
			k = k//2

	def swap(self, i, j):
		'''
		swaps two elements in an array
		:param i, j: integers, position of items to be swaped
		:complexity: O(1)
		'''
		temp = self.array[i]
		self.array[i] = self.array[j]
		self.array[j] = temp 

	def __str__(self):
		string = '' 
		for i in range(self.count):
			string += str(self.array[i+1])
		return string

	def serve(self):
		'''
		returns item of smallest key in the heap
		:return: item of any type
		:complexity: best = O(1), worst = O(log N), where N = depth of heap
		'''
		assert not self.is_empty(), "Can't serve from empty list"
		item = self.array[1]
		self.swap(1, self.count)
		self.count -= 1

		self.sink()
		return item

	def sink(self):
		'''
		brings item on top of heap to the position where it belongs
		:complexity: best = O(1), worst = O(log k)
		'''
		k = 1
		while (k*2 <= self.count):
			child = self.get_smallest_child(k)
			if self.array[k][0] < self.array[child][0]:
				break	
			self.swap(k, child)
			k = child

	def get_smallest_child(self, i):
		'''
		param i: integer, position of node
		return: integer, position of child with smallest key
		complexity: O(1)
		'''
		try:
			assert (i*2+1)<=self.count
		except AssertionError:
			return i*2
		if self.array[i*2] < self.array[i*2+1]:
			return i*2
		else:
			return i*2+1

def menu():
    '''
    
    '''
    quit = False
    heap = MinHeap()
    while not quit:
        commands = [0, 1, 2, 3, 4]
        print(
                '''
                ---Binary Tree Class menu---
                Available commands:
                1 	apend 
                2 	serve
                3 	print
                4   size
                0 	quit
                '''
                )

        command = input('Enter command: ')
        try:
        	command = int(command)
        	assert command in commands
        except (ValueError, AssertionError):
            print('Unknown command, try again')
        else:
            if command == 1:
            	item = input('Enter item: ')
            	heap.append([item])
            elif command == 2:
                print(heap.serve())
            elif command == 3:
                print(str(heap))
            elif command == 4:
                print(len(heap))
            elif command == 0:
                quit = True

def main():
	menu()

if __name__ == '__main__':
	main()