from mrjob.job import MRJob
from mrjob.step import MRStep

class FrequencyAuthors(MRJob):
    def steps(self):# MRjob could consist of several steps
        return [MRStep(mapper=self.mapper_get_ratings,
                       reducer=self.reducer_count_ratings),
                MRStep(reducer=self.reducer_sorted_output)]

    def mapper_get_ratings(self, _, line):
        (_id, ressort, date) = line.split('\t')
        yield ressort, 1
    '''
    "Politik" 1
    "Kultur" 1
    "Kultur" 1 
    "Ökologie" 1   
    '''

    def reducer_count_ratings(self, key, values):
        yield str(sum(values)).zfill(5), key
    '''
    "Politik" "00001"
    "Kultur" "00002"
    "Ökologie" "00001"
    '''

    def reducer_sorted_output(self, count, ressorts):
        for ressort in ressorts:
            yield ressort, count
    '''
    "Ökologie" "00001"
    "Politik" "00001"
    "Kultur" "00002"
    '''

if __name__ == '__main__':FrequencyAuthors.run()