import numpy as np
import time
import cProfile
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
		self.data = np.load('train_small_10.npy')
		self.test_data = np.load('test_small_10.npy')
		print (self.data)
		self.user_data = {}
		self.movie_data = {}
		self.cache = {}
		self.relations = None
		return
		
	def mean_rating(self):
		idx = np.lexsort(data[:, :2].T)
		data = data[idx, :]
	
	
	#Stores in format of user_data[user_id][movie_id] = rating for movie
	def build_userdata(self):
		num_users = len(self.data)
		for i in range(len(self.data)):
		
			try:
				self.user_data[self.data[i][0]][self.data[i][1]] = self.data[i][2]
			except KeyError:
				self.user_data[self.data[i][0]] = {}
				self.user_data[self.data[i][0]][self.data[i][1]] = self.data[i][2]
				
			try:
				self.movie_data[self.data[i][1]].append(self.data[i][0])
			except KeyError:
				self.movie_data[self.data[i][1]] = [self.data[i][0]]
			#print('%5.1f%%' % (100 * i / num_users), end='\r')
			#self.user_data[self.data[i][0]].append(data[i][1:2])
	
				
	def build_movedata(self):
		for i in range(len(self.data)):
			#movie_data[self.data[i][1]].append(self.data[i][0::2])
			movie_data[self.data[i][1]][self.data[i][0]] = self.data[i][2]
	
	def build_relations(self):
		num_users = len(self.user_data)
		a = np.zeros((num_users,num_users))
		for i in range(num_users):
			#print('%5.1f%%' % (100 * i / num_users), end='\r')
			for j in range((i+1),num_users):
				
				a[j][i] = a[i][j]= self.compare_users(i,j)
				
	def predict(self,target_user,movie):
		temp = [0] * len(self.movie_data[movie])
		#print (self.movie_data[movie])
		prediction = 0
		for i in range(len(self.movie_data[movie])):
			if target_user == self.movie_data[movie][i]:
				continue
			temp[i] = self.compare_users(self.movie_data[movie][i],target_user)
			#print (i)
		
		#print (movie,target_user,np.amax(temp))
		proxy_user = self.movie_data[movie][np.argmax(temp)]
		#print (movie,target_user,proxy_user,np.argmax(temp))
		#print (self.user_data[proxy_user])
		try:
			prediction = self.user_data[proxy_user][movie] 
		except KeyError:
			print (proxy_user,"has not rated movie",movie)
			print (movie in self.user_data[proxy_user].keys())
			print (proxy_user in self.movie_data[movie])
		return round(prediction)
		
		
	def test_model(self):
		#num_cols = len(self.test_data[0])
		total = 0
		correct = 0
		size = len(self.test_data)
		print (size)
		for i in range(len(self.test_data)):
			if i % 100 == 0:
				print (i/size)
			if self.test_data[i][2] == self.predict(self.test_data[i][0],self.test_data[i][1]):
				correct += 1
			total += 1 
		
		print (correct,"out of",total,"correct")
			
			
				
	def get_common_movies(self,root_user,other_user):
		return self.user_data[root_user].keys() & self.user_data[other_user].keys()
	
	def compare_users(self,root_user,other_user):
		try:
			ans = self.cache[root_user][other_user]
			return ans
		except KeyError:
			pass
		tolerance_rating = 1 #Tolerance for difference a rating can be considered as similar 
		similar = 0 
		same_movies = self.get_common_movies(root_user,other_user)
		for movie in same_movies:
			total = self.user_data[root_user][movie] - self.user_data[other_user][movie]
			if abs(total) < tolerance_rating:
					similar += 1
		try:
			self.cache[root_user][other_user] = similar
		except KeyError:
			self.cache[root_user] = {}
			self.cache[root_user][other_user] = similar
			
		try:
			self.cache[other_user][root_user] = similar
		except KeyError:
			self.cache[other_user] = {}
			self.cache[other_user][root_user] = similar
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
	print (n.test_data)
	n.build_userdata()
	#n.build_relations()
	n.test_model()
	
#main()
#cProfile.run("main()")		
		
def model():
	data = np.load('train_small_10.npy')
	t0 = time.time()
	num_users = np.max(data[:, 0], axis=0) + 1
	u = np.zeros((num_users, 1))
	k0 = 0
	
	#u is the u[user_id] = average rating for user
	for j in range(num_users):
		#print('%5.1f%%' % (100 * j / num_users), end='\r')
		k1 = k0 + 1
		while k1 < len(data) and data[k1, 1] == j:
			k1 += 1
		u[j] = np.mean(data[k0:k1, 2])
		k0 = k1
	print (u)
	
	index = np.lexsort(data[:, :2].T)
	data = data[index, :]

	num_movies = np.max(data[:, 1], axis=0) + 1
	print('%d movies' % num_movies)

	h = np.zeros((num_movies, 1))
	print (data)

	k0 = 0
	
	
	#h is the h[movie_id] = average rating for movie
	for j in range(num_movies):
		#print('%5.1f%%' % (100 * j / num_movies), end='\r')
		k1 = k0 + 1
		while k1 < len(data) and data[k1, 1] == j:
			k1 += 1
		h[j] = np.mean(data[k0:k1, 2])
		k0 = k1
		
	print (h)



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
	return h,u
	
def test_model(h):
		#num_cols = len(self.test_data[0])
		test_data = np.load('test_small_10.npy')
		print (h)
		total = 0
		correct = 0
		size = len(test_data)
		print (size)
		for i in range(len(test_data)):
			if i % 100 == 0:
				print (i/size)
			prediction = test_data[i][1]
			if prediction == None:
				prediction = 0
			if test_data[i][2] == int(h[prediction]):
				correct += 1
			total += 1 
		
		print (correct,"out of",total,"correct")
		
def test_model2(h):
		#num_cols = len(self.test_data[0])
		test_data = np.load('test_small_10.npy')
		print (h)
		total = 0
		correct = 0
		size = len(test_data)
		print (size)
		for i in range(len(test_data)):
			if i % 100 == 0:
				print (i/size)
			prediction = test_data[i][0]
			if prediction == None:
				prediction = 0
			if test_data[i][2] == int(h[prediction]):
				correct += 1
			total += 1 
		
		print (correct,"out of",total,"correct")

'''	
h,u = model()
test_model(h)
test_model2(u)
'''
		
		
		
