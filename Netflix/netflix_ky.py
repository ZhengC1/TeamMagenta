import numpy as np
import time

'''
class User:
	def __init__(self):
		self.movies = []
		self.ratings = []
		return
		
	def add_data(self,movie_data):
		#print (movie_data)
		self.movies.append(movie_data[0])
		self.ratings.append(movie_data[1])
'''

class Netflix:
	def __init__(self):
		self.data = np.load('train.npy')
		self.user_data = {}
		return
		
	def mean_rating(self):
		idx = np.lexsort(data[:, :2].T)
		data = data[idx, :]
	
	
	#Stores in format of user_data[user_id][movie_id] = rating for movie
	def build_userdata(self):
		num_users = len(self.data)
		prev = -1
		for i in range(len(self.data)):
			if self.data[i][0] != prev:
				self.user_data[self.data[i][0]] = {}
			self.user_data[self.data[i][0]][self.data[i][1]] = self.data[i][2]
			print('%5.1f%%' % (100 * i / num_users), end='\r')
			prev = i
			#self.user_data[self.data[i][0]].append(data[i][1:2])
	
				
	def build_movedata(self):
		for i in range(len(self.data)):
			#movie_data[self.data[i][1]].append(self.data[i][0::2])
			movie_data[self.data[i][1]][self.data[i][0]] = self.data[i][2]
	
	def build_relations(self):
		num_users = len(self.users)
		for i in range(num_users):
			for j in range((i+1),num_users):
				compare_users(i,j)
				
				
	
	def compare_users(self,root_user,other_user):
		tolerance_rating = 1 #Tolerance for difference a rating can be considered as similar 
		similar = 0 
		same_movies = root_user.keys() & other_user.keys()
		for movie in same_movies:
			total = self.user_data[root_user][movie] - self.user_data[other_user][movie]
			if abs(total) < tolerance_rating:
					similar += 1
		return similar
			
				
	def find_similar_user(self,root_user):
		tolerance_similar = 2
		similar_users = []
		most_similar = 0
		for user in self.user_data:
			if user != root_user:
				common = self.compare_users(root_user,user)
				if common > tolerance_similar:
					if most_similar < common:
						most_similar = common
					similar_users.append([user,common])
		a = np.array(similar_users)
		print (len(a))
		return
				

		
def main():
	n = Netflix()
	print (len(n.data))
	n.build_userdata()
	
	n.find_similar_user(0)
	
main()
	
		
def model():
	data = np.load('train.npy')
	t0 = time.time()

	index = np.lexsort(data[:, :2].T)
	data = data[index, :]

	num_movies = np.max(data[:, 1], axis=0) + 1
	print('%d movies' % num_movies)

	h = np.zeros((num_movies, 1))

	k0 = 0
	for j in range(num_movies):
		print('%5.1f%%' % (100 * j / num_movies), end='\r')
		k1 = k0 + 1
		while k1 < len(data) and data[k1, 1] == j:
			k1 += 1
		h[j] = np.mean(data[k0:k1, 2])
		k0 = k1


	#for j in range(num_movies):
	#    index = data[:, 1] == j
	#    h[j] = len(data[index, :])

	#for row in data:
	#    j = row[1]
	#    h[j] += 1


	j = np.argmin(h, axis=0)

	print('%d ratings for movie %d' % (h[j], j))
	t1 = time.time()
	print('%f seconds' % (t1 - t0))
#model()
		
		
		