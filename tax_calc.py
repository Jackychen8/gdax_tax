import csv

class trades():

	def __init__(self):
		self.trans = {}
		# use 'trade id' as key


	def load_csv(self, file_name):
		with open(file_name, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			'''
			type time amount balance unit TransferId TradeId OrderId
			ty   ti   am     bal     un   i          j       o 
			'''
			for ty, ti, am, bal, un, i, j, o in reader:
				if not i: # we don't care about transfers
					if j in self.trans:
						self.trans[j][un] = float(am)
						self.trans[j]['time'] = ti
					else:
						self.trans[j] = {un: float(am), 'time': ti}


	def load_csvs(self, files_list=[]):
		for file in files_list:
			self.load_csv(file)


	def calc_p(self):
		it = self.trans.iteritems()
		for item in it:
			d = item[1]
			if 'USD' not in d or len(d) < 2:
				print('Error: transaction data issues: %r' %d)
				break
			else:
				other = 'ETH' if 'ETH' in d else 'LTC'
				self.trans[item[0]]['price'] = abs(d['USD']/d[other])
				self.trans[item[0]]['type'] = 'buy' if d['USD'] < 0.0 else 'sell'

	def export_csv(self, file_name = '~/Documents/gdax/ex.csv'):
		with open(file_name, 'wb') as csvfile:
			f = ['id', 'coin', 'Crypto', 'USD', 'type', 'price', 'time']
			writer = csv.DictWriter(csvfile, fieldnames=f)
			writer.writeheader()

			for i, info in self.trans.iteritems():
				ty = 'ETH' if 'ETH' in info else 'LTC'
				d = {
					'id': i,
					'coin': ty,
					'Crypto': info[ty],
					'USD': info['USD'],
					'type': info['type'], 
					'price': info['price'], 
					'time': info['time']
				}
				writer.writerow(d)

	def print_stats(self, type='USD'):
		for item in self.trans.iteritems():
			if type in item[1]:
				print item

# if __name__ == '__main__':
# 	# calc tax
# A = t()
# A.load_csv('~/Downloads/eth_gdax_account.csv')
# A.calc_p()
# A.print_stats()