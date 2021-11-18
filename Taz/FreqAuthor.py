from mrjob.job import MRJob
from mrjob.step import MRStep

class FrequencyAuthors(MRJob):
    def steps(self):# MRjob could consist of several steps
        return [MRStep(mapper=self.mapper_get_ratings,
                       reducer=self.reducer_count_ratings),
                MRStep(reducer=self.reducer_sorted_output)]

    def mapper_get_ratings(self, _, line):
        (_id, author, date) = line.split('\t')
        yield author, 1
    '''
    "Guido" 1
    "Peter" 1
    "Peter" 1 
    "Lisa" 1   
    '''

    def reducer_count_ratings(self, key, values):
        yield str(sum(values)).zfill(5), key
    '''
    "Guido" "00001"
    "Peter" "00002"
    "Lisa" "00001"
    '''

    def reducer_sorted_output(self, count, authors):
        for author in authors:
            yield author, count
    '''
    "Guido" "00001"
    "Lisa" "00001"
    "Peter" "00002"
    '''

if __name__ == '__main__':FrequencyAuthors.run()