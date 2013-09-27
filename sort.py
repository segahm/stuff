
import random
import sys
import time

#O(nlogn), O(nlogn), O(nlogn)
def mergesort(array):
    if len(array) <= 1:
        return array
    middle = len(array)//2
    left = []
    right = []
    for item in array[:middle]:
        left.append(item)
    for item in array[middle:]:
        right.append(item)
    
    return merge(mergesort(left),mergesort(right))

def merge(a,b):
    result = [0]*(len(a)+len(b))
    indx = 0
    while len(a) > 0 or len(b) >0:
        if len(a) > 0 and len(b) >0:
            if a[0] <= b[0]:
                result[indx] = a.pop(0) #a's element is smaller
            else:
                result[indx] = b.pop(0) #b is smaller
        elif len(a) > 0:
            result[indx:indx+len(a)]    =   a    #no more b elements left
            a = []  #clear the pointer
        elif len(b) > 0:
            result[indx:indx+len(b)]    =   b
            b = []
        indx += 1
    return result


#O(nlogn), O(nlogn), O(n^2)
def quicksort(array):
    if len(array) <= 1:
        return array
    #choose a random pivot
    pivot = random.randint(0,len(array)-1)
    pivot = array.pop(pivot)
    less = []
    greater = []
    for item in array:
        if item <= pivot:
            less.append(item)
        else:
            greater.append(item)
    array = quicksort(less)
    array.append(pivot)
    array.extend(quicksort(greater))
    return array

#O(n), O(n^2), O(n^2)
def insertsort(array):
    if len(array) <= 1:
        return array
    for indx,v in enumerate(array):
        temp = v
        j = indx-1
        while j >= 0 and temp <= array[j]:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = temp
    return array

#O(n^2), O(n^2), O(n^2)
def selectionsort(array):
    for k,v in enumerate(array):
        iMin = k
        i = k+1
        while i < len(array):
            if array[i] < array[iMin]:
                iMin = i
            i += 1
        if iMin != k:
            temp = array[iMin]
            array[iMin] = array[k]
            array[k] = temp
    return array

#O(n+k)
def pigeonhole(array): 
    holes = []
    i_min = min(array)  #n-1
    i_max = max(array)  #n-1
    holes = [0]*(i_max-i_min+1) #c1
    for a in array:             #n
        holes[a-i_min] += 1
    print "holes 2:", holes
    j = 0
    for i,v in enumerate(holes):    #k+n
        while holes[i] > 0:
            array[j] = i
            j += 1
            holes[i] -= 1
    return array


def main():
    min = 1
    max = 100
    count = 20
    
    if len(sys.argv) >= 2:
        operation = sys.argv[1]
    else:
        print 'quicksort.py quicksort/mergesort --[count] --[min] --[max]'
        sys.exit()


    if len(sys.argv) >= 3:
        count = int(sys.argv[2])
    if len(sys.argv) >= 4:
        min = int(sys.argv[3])
    if len(sys.argv) >= 5:
        max = int(sys.argv[4])


    #generate random array
    array = [0]*count
    while count > 0:
        array[-count] = random.randint(min,max)
        count -= 1
    time.clock()
    #print 'original: ',array
    if operation == 'quicksort':
        print 'quicksort'
        array = quicksort(array)
    elif operation == 'mergesort':
        print 'mergesort'
        array = mergesort(array)
    elif operation == 'insertsort':
        print 'insertion'
        array = insertsort(array)
    elif operation == 'selectionsort':
        print 'selection'
        array = selectionsort(array)
    elif operation == 'pigeon':
        print 'pigeon'
        array = pigeonhole(array)
    else:
        print 'quicksort.py quicksort/mergesort --[count] --[min] --[max]'
        sys.exit()
    #elif operation == 'selection':

    print 'final: ',array
    print 'time: ', time.clock()


if __name__ == '__main__':
    main()