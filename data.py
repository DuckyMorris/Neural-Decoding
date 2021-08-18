class Data():
    '''
    Defined type of 3 arrays of length being the number of neurons and the length of each entry is the number of
    samples
    '''
    def __init__(self):
        self.sampled_data = []
        self.labels = []
        self.time_stamps = []
    
    def bin_data(self, bin_size, sample_rate):
        '''
        Calculates the average firing rates in 150 ms bins sampled every 50 ms, the following commands can be used.
        Returns a data object but in a binned form
        '''
        binned = Data()
        
        for x in range(len(self.sampled_data)):
            binned_array = []
            stamps = []
            labels = []
            y = 0
            while True:
                bin = sum(self.sampled_data[x][y:y+bin_size]) / bin_size
                binned_array.append(bin)
                try:
                    labels.append(self.labels[x][y])
                except:
                    print(x)
                    print(y)
                    print(len(self.labels))
                    print(len(self.labels[x]), len(self.sampled_data[x]))
                    exit()
                stamps.append(y)
                if y + sample_rate >= len(self.sampled_data[x]):
                    break
                else:
                    y = y+sample_rate
            
            binned.sampled_data.append(binned_array)
            binned.time_stamps.append(stamps)
            binned.labels.append(labels)

        return binned