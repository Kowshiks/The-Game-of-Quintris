import math
import random
import matplotlib.pyplot as plt

def naive(m):
    
    # OPEN THE FILE AND READ THE LINES 
    result_list = []
    
    for file_name in ['pp1data/amazon_cells_labelled.txt','pp1data/imdb_labelled.txt', 'pp1data/yelp_labelled.txt']:
    
        file = open(file_name, 'r')
        lines = file.readlines()

        #SHUFFLE THE LINES IN THE FILE
        random.shuffle(lines)
        
        avg_sd = {}
        accuracy_list = []
        sub_sample_dict = {}

        size_X = []
        accuracy_Y = []
        standard_deviation_Y = []


        # 10 FOLD STRATIFIED CROSS VALIDATION
        for fold in range(10):

            positive_fold = []
            negative_fold = []


            #LOOPING THROUGH EACH SENTENCE IN THE FILE
            for each_fold in lines:
                if each_fold.split()[-1] == "0":
                    negative_fold.append(each_fold)  # ALL THE NEGATIVE SENTENSES ARE ADDED INTO A SEPARATE LIST

                else:
                    positive_fold.append(each_fold)  # ALL THE POSITIVE SENTENSES ARE ADDED INTO A SEPARATE LIST


            # BOTH POSITIVE AND NEGATIVE LISTS ARE RANDOMLY SHUFFLED AGAIN
            random.shuffle(positive_fold)
            random.shuffle(negative_fold)


            # THE TRAIN TEST SPLIT COUNT IS SET TO 0.5, WHERE IT HAS EQUAL LENGTH OF TRAIN AND TEST DATA
            train_test_fold_split = 0.5


            # THE INDEX FOR SPLITTING THE POSITIVE AND NEGATIVE LIST
            pos_fold_index = round(train_test_fold_split * len(positive_fold))
            neg_fold_index = round(train_test_fold_split * len(negative_fold))


            # THE TRAINING DATA 
            fold_train_data = positive_fold[:pos_fold_index] + negative_fold[:neg_fold_index]

            # THE TESTING DATA
            fold_test_data = positive_fold[pos_fold_index:] + negative_fold[neg_fold_index:] 

            # AGAIN THE TRAINING DATA IS SHUFFLED
            random.shuffle(fold_train_data)

            sample_index = 1

            # FOR LEARNING CURVES THE SUB SAMPLE ARE TAKEN FROM THE TRAINING DATA
            for sample in range(10):

                total_positive = 0
                total_negative = 0


                # THE SUB SAMPLE SPLIT COUNT IS CALCULATED [ 0.1N, 0.2N, 0.3N ........ N]
                sub_sample_index = sample_index/10

                # SUB SAMPLE COUNT INDEX IS ADDED INTO A DICTIONARY
                if sub_sample_index not in sub_sample_dict.keys():
                    sub_sample_dict[sub_sample_index] = []


                # THE INDEX FOR SPLITTING THE TRAINING DATA WITH THE ACQUIRED COUNT INDEX ABOVE
                parse_index = round(len(fold_train_data) * sub_sample_index)


                # THE SUB SAMLPED TRAINING DATA
                fold_train_data_sample = fold_train_data[:parse_index]


                #TRAIN

                positive_words = []
                negative_words = []

                total_positive = 0
                total_negative = 0

                # THE LINES IN THE TRAIN LIST ARE LOOPED AND PARSED TO GET THE WORDS WITHOUT ANY EXTRA SYMBOLS
                for each_line in fold_train_data_sample:

                    if each_line.split()[-1] == "0": 

                        for each_word in each_line.split()[:-1]:

                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_negative+=1
                                negative_words.append(parsed_word)  # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST

                    else:

                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_positive+=1
                                positive_words.append(parsed_word)  # ALL THE POSITIVE WORDS ARE APPENDED INTO THE LIST


                n_positive = len(positive_words)
                n_negative = len(negative_words)


                # VOCABULORY OF NEGATIVE AND POSITIVE WORDS ARE CALCULATED 
                v_positive = len(set(positive_words))
                v_negative = len(set(negative_words))

                positive_dict = {}
                negative_dict = {}

                pos_estimate = {}
                neg_estimate = {}

                initial_num = 1

                # UNION OF ALL THE NEGATIVE AND POSITIVE WORDS
                all_data = set(positive_words).union(set(negative_words))


                # COUNT THE NUMBER OF UNIQUE POSITIVE WORDS AND ADD THE WORD AS THE KEY AND THE COUNT AS A VALUE IN A DICTIONARY
                for each_pos in positive_words:  
                    if each_pos not in positive_dict.keys():
                        positive_dict[each_pos] = initial_num
                    if each_pos in positive_dict.keys():
                        positive_dict[each_pos] = positive_dict[each_pos]+1


                # COUNT THE NUMBER OF UNIQUE NEGATIVE WORDS AND ADD THE WORD AS THE KEY AND THE COUNT AS A VALUE IN A DICTIONARY
                for each_neg in negative_words:
                    if each_neg not in negative_dict.keys():
                        negative_dict[each_neg] = initial_num
                    else:
                        negative_dict[each_neg] = negative_dict[each_neg]+1


                # ADD ALL THE WORDS THAT ARE NOT PRESENT IN EACH OF THE POSITIVE NEGATIVE LIST TO THE THE OTHER COUNT DICTIONARY AND ASSIGN THE COUNT TO 0
                for each_value in all_data:
                    if each_value not in negative_dict.keys():
                        negative_dict[each_value] = 0

                    if each_value not in positive_dict.keys():
                        positive_dict[each_value] = 0


                # PRIOR FOR THE POSITIVE WORDS
                prior_pos = total_positive / (total_positive+total_negative)
                #PRIOR FOR NEGATIVE WORDS
                prior_neg = total_negative / (total_positive+total_negative)


                # THE MLE AND MAP ESTIMATES DEPENDING ON THE GIVEN M 
                for key,value in positive_dict.items():
                    pos_estimate[key] = (value + m)/(n_positive + (m*v_positive))


                for key,value in negative_dict.items():
                    neg_estimate[key] = (value + m)/(n_negative + (m*v_negative))




                #TEST

                negative_words_test = []
                positive_words_test = []

                total_negative_test = 0
                total_positive_test = 0


                # THE LINES IN THE TEST LIST ARE LOOPED AND PARSED TO GET THE WORDS WITHOUT ANY EXTRA SYMBOLS
                for each_line in fold_test_data:

                    if each_line.split()[-1] == "0":
                        parsed_word_list = []
                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_negative_test += 1

                                parsed_word_list.append(parsed_word)
                        negative_words_test.append(parsed_word_list)    # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST


                    else:

                        parsed_word_list = []
                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_positive_test += 1

                                parsed_word_list.append(parsed_word)
                        positive_words_test.append(parsed_word_list)   # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST


                true_predict = 0
                false_predict = 0


                # THE MAP AND MLE ARE PREDICTED BASED ON THE PROVIDED M AND CHECKED IF THEY ARE POSITIVE (LOG IS TAKEN HERE)
                for each_line in positive_words_test:

                    weight_pos = math.log(prior_pos)

                    weight_neg = math.log(prior_neg)

                    for each_word in each_line:

                        if each_word in pos_estimate.keys(): 
                            if pos_estimate[each_word] == 0.0:
                                weight_pos = weight_pos + float(-math.inf)    # MLE IS PREDICTED IN POSITIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_pos = weight_pos + math.log(pos_estimate[each_word]) # MAP IS PREDICTED IN POSITIVE LIST

                        if each_word in neg_estimate.keys():
                            if neg_estimate[each_word] == 0.0:
                                weight_neg = weight_neg + float(-math.inf)    # MLE IS PREDICTED IN NEGATIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_neg = weight_neg + math.log(neg_estimate[each_word])  # MAP IS PREDICTED IN NEGATIVE LIST

                    if(weight_pos > weight_neg): # CORRECTLY PREDICTS
                        true_predict+=1

                    else:                        # WRONGLY PREDICTS
                        false_predict+=1



                true_predict_1 = 0
                false_predict_1 = 0


                # THE MAP AND MLE ARE PREDICTED BASED ON THE PROVIDED M AND CHECKED IF THEY ARE NEGATIVE (LOG IS TAKEN HERE)
                for each_line in negative_words_test:

                    weight_neg = math.log(prior_neg)
                    weight_pos = math.log(prior_pos)

                    for each_word in each_line:
                        if each_word in neg_estimate.keys():
                            if neg_estimate[each_word] == 0.0:
                                weight_neg = weight_neg + float(-math.inf)     # MLE IS PREDICTED IN NEGATIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_neg = weight_neg + math.log(neg_estimate[each_word])      # MAP IS PREDICTED IN NEGATIVE LIST

                        if each_word in pos_estimate.keys():
                            if pos_estimate[each_word] == 0.0:
                                weight_pos = weight_pos + float(-math.inf)     # MLE IS PREDICTED IN POSITIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_pos = weight_pos + math.log(pos_estimate[each_word])      # MAP IS PREDICTED IN POSITIVE LIST

                    if(weight_neg > weight_pos):   # CORRECTLY PREDICTS 
                        true_predict_1 +=1

                    else:
                        false_predict_1 +=1        # WRONGLY PREDICTS


                # TOTAL CORRECTLY PREDICTED LINES
                true_data = true_predict_1 + true_predict
                # TOTAL WRONGLY PREDICTED LINES
                false_data = false_predict + false_predict_1

                #THE ACCURACY
                accuracy = true_data/(true_data+false_data)

                sub_sample_dict[sub_sample_index].append(accuracy)

                if(len(size_X) < 10):
                    size_X.append(parse_index)

                sample_index+=1
        

        for key,values in sub_sample_dict.items():

            each_size = {}

            mean = sum(values)/10
            variance = sum([((each_sample - mean) ** 2) for each_sample in values]) / len(values)

            each_size["average"] = mean
            each_size["standard deviation"] = math.sqrt(variance)

            accuracy_Y.append(mean)
            standard_deviation_Y.append(math.sqrt(variance))

            avg_sd[key] = each_size

        result_list.append((size_X, accuracy_Y, standard_deviation_Y))
        
    return result_list


def smoothing_param(m_list):
    
    graph_details = {}
    
    for file_name in ['pp1data/amazon_cells_labelled.txt','pp1data/imdb_labelled.txt', 'pp1data/yelp_labelled.txt']:
    
        # OPEN THE FILE AND READ THE LINES 
        file = open(file_name, 'r')
        lines = file.readlines()

        #SHUFFLE THE LINES IN THE FILE
        random.shuffle(lines)

        for m in m_list:

            avg_sd = {}
            accuracy_list = []
            sub_sample_dict = {}

            size_X = []
            accuracy_Y = []
            standard_deviation_Y = []
            
            each_accuracy_list = []
            
            each_graph_details = {}


            # 10 FOLD STRATIFIED CROSS VALIDATION
            for fold in range(10):

                positive_fold = []
                negative_fold = []


                #LOOPING THROUGH EACH SENTENCE IN THE FILE
                for each_fold in lines:
                    if each_fold.split()[-1] == "0":
                        negative_fold.append(each_fold)  # ALL THE NEGATIVE SENTENSES ARE ADDED INTO A SEPARATE LIST

                    else:
                        positive_fold.append(each_fold)  # ALL THE POSITIVE SENTENSES ARE ADDED INTO A SEPARATE LIST


                # BOTH POSITIVE AND NEGATIVE LISTS ARE RANDOMLY SHUFFLED AGAIN
                random.shuffle(positive_fold)
                random.shuffle(negative_fold)


                # THE TRAIN TEST SPLIT COUNT IS SET TO 0.5, WHERE IT HAS EQUAL LENGTH OF TRAIN AND TEST DATA
                train_test_fold_split = 0.5


                # THE INDEX FOR SPLITTING THE POSITIVE AND NEGATIVE LIST
                pos_fold_index = round(train_test_fold_split * len(positive_fold))
                neg_fold_index = round(train_test_fold_split * len(negative_fold))


                # THE TRAINING DATA 
                fold_train_data = positive_fold[:pos_fold_index] + negative_fold[:neg_fold_index]

                # THE TESTING DATA
                fold_test_data = positive_fold[pos_fold_index:] + negative_fold[neg_fold_index:] 

                # AGAIN THE TRAINING DATA IS SHUFFLED
                random.shuffle(fold_train_data)

                sample_index = 1

                total_positive = 0
                total_negative = 0

                #TRAIN

                positive_words = []
                negative_words = []

                total_positive = 0
                total_negative = 0

                # THE LINES IN THE TRAIN LIST ARE LOOPED AND PARSED TO GET THE WORDS WITHOUT ANY EXTRA SYMBOLS
                for each_line in fold_train_data:

                    if each_line.split()[-1] == "0": 

                        for each_word in each_line.split()[:-1]:

                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_negative+=1
                                negative_words.append(parsed_word)  # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST

                    else:

                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_positive+=1
                                positive_words.append(parsed_word)  # ALL THE POSITIVE WORDS ARE APPENDED INTO THE LIST


                n_positive = len(positive_words)
                n_negative = len(negative_words)


                # VOCABULORY OF NEGATIVE AND POSITIVE WORDS ARE CALCULATED 
                v_positive = len(set(positive_words))
                v_negative = len(set(negative_words))

                positive_dict = {}
                negative_dict = {}

                pos_estimate = {}
                neg_estimate = {}

                initial_num = 1

                # UNION OF ALL THE NEGATIVE AND POSITIVE WORDS
                all_data = set(positive_words).union(set(negative_words))


                # COUNT THE NUMBER OF UNIQUE POSITIVE WORDS AND ADD THE WORD AS THE KEY AND THE COUNT AS A VALUE IN A DICTIONARY
                for each_pos in positive_words:  
                    if each_pos not in positive_dict.keys():
                        positive_dict[each_pos] = initial_num
                    if each_pos in positive_dict.keys():
                        positive_dict[each_pos] = positive_dict[each_pos]+1


                # COUNT THE NUMBER OF UNIQUE NEGATIVE WORDS AND ADD THE WORD AS THE KEY AND THE COUNT AS A VALUE IN A DICTIONARY
                for each_neg in negative_words:
                    if each_neg not in negative_dict.keys():
                        negative_dict[each_neg] = initial_num
                    else:
                        negative_dict[each_neg] = negative_dict[each_neg]+1


                # ADD ALL THE WORDS THAT ARE NOT PRESENT IN EACH OF THE POSITIVE NEGATIVE LIST TO THE THE OTHER COUNT DICTIONARY AND ASSIGN THE COUNT TO 0
                for each_value in all_data:
                    if each_value not in negative_dict.keys():
                        negative_dict[each_value] = 0

                    if each_value not in positive_dict.keys():
                        positive_dict[each_value] = 0


                # PRIOR FOR THE POSITIVE WORDS
                prior_pos = total_positive / (total_positive+total_negative)
                #PRIOR FOR NEGATIVE WORDS
                prior_neg = total_negative / (total_positive+total_negative)


                # THE MLE AND MAP ESTIMATES DEPENDING ON THE GIVEN M 
                for key,value in positive_dict.items():
                    pos_estimate[key] = (value + m)/(n_positive + (m*v_positive))


                for key,value in negative_dict.items():
                    neg_estimate[key] = (value + m)/(n_negative + (m*v_negative))




                #TEST

                negative_words_test = []
                positive_words_test = []

                total_negative_test = 0
                total_positive_test = 0


                # THE LINES IN THE TEST LIST ARE LOOPED AND PARSED TO GET THE WORDS WITHOUT ANY EXTRA SYMBOLS
                for each_line in fold_test_data:

                    if each_line.split()[-1] == "0":
                        parsed_word_list = []
                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_negative_test += 1

                                parsed_word_list.append(parsed_word)
                        negative_words_test.append(parsed_word_list)    # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST


                    else:

                        parsed_word_list = []
                        for each_word in each_line.split()[:-1]:
                            parsed_word = ''.join(filter(str.isalpha, each_word)).lower()
                            if parsed_word:
                                total_positive_test += 1

                                parsed_word_list.append(parsed_word)
                        positive_words_test.append(parsed_word_list)   # ALL THE NEGATIVE WORDS ARE APPENDED INTO THE LIST


                true_predict = 0
                false_predict = 0


                # THE MAP AND MLE ARE PREDICTED BASED ON THE PROVIDED M AND CHECKED IF THEY ARE POSITIVE (LOG IS TAKEN HERE)
                for each_line in positive_words_test:

                    weight_pos = math.log(prior_pos)

                    weight_neg = math.log(prior_neg)

                    for each_word in each_line:

                        if each_word in pos_estimate.keys(): 
                            if pos_estimate[each_word] == 0.0:
                                weight_pos = weight_pos + float(-math.inf)    # MLE IS PREDICTED IN POSITIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_pos = weight_pos + math.log(pos_estimate[each_word]) # MAP IS PREDICTED IN POSITIVE LIST

                        if each_word in neg_estimate.keys():
                            if neg_estimate[each_word] == 0.0:
                                weight_neg = weight_neg + float(-math.inf)    # MLE IS PREDICTED IN NEGATIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_neg = weight_neg + math.log(neg_estimate[each_word])  # MAP IS PREDICTED IN NEGATIVE LIST

                    if(weight_pos > weight_neg): # CORRECTLY PREDICTS
                        true_predict+=1

                    else:                        # WRONGLY PREDICTS
                        false_predict+=1



                true_predict_1 = 0
                false_predict_1 = 0


                # THE MAP AND MLE ARE PREDICTED BASED ON THE PROVIDED M AND CHECKED IF THEY ARE NEGATIVE (LOG IS TAKEN HERE)
                for each_line in negative_words_test:

                    weight_neg = math.log(prior_neg)
                    weight_pos = math.log(prior_pos)

                    for each_word in each_line:
                        if each_word in neg_estimate.keys():
                            if neg_estimate[each_word] == 0.0:
                                weight_neg = weight_neg + float(-math.inf)     # MLE IS PREDICTED IN NEGATIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_neg = weight_neg + math.log(neg_estimate[each_word])      # MAP IS PREDICTED IN NEGATIVE LIST

                        if each_word in pos_estimate.keys():
                            if pos_estimate[each_word] == 0.0:
                                weight_pos = weight_pos + float(-math.inf)     # MLE IS PREDICTED IN POSITIVE LIST(HERE THE LOG(0) IS HANDLED BY GIVING -INF AS THE VALUE)
                            else:
                                weight_pos = weight_pos + math.log(pos_estimate[each_word])      # MAP IS PREDICTED IN POSITIVE LIST

                    if(weight_neg > weight_pos):   # CORRECTLY PREDICTS 
                        true_predict_1 +=1

                    else:
                        false_predict_1 +=1        # WRONGLY PREDICTS


                # TOTAL CORRECTLY PREDICTED LINES
                true_data = true_predict_1 + true_predict
                # TOTAL WRONGLY PREDICTED LINES
                false_data = false_predict + false_predict_1

                #THE ACCURACY
                accuracy = true_data/(true_data+false_data)
                
                if m not in each_graph_details.keys():
                    each_graph_details[m] = []
                    each_graph_details[m].append(accuracy)
                else:
                    each_graph_details[m].append(accuracy)
                
            if m not in graph_details.keys():
                
                
                mean = sum(each_graph_details[m])/10
                variance = sum([((each_sample - mean) ** 2) for each_sample in each_graph_details[m]]) / len(each_graph_details[m])
                
                graph_details[m] = []
                graph_details[m].append(each_graph_details[m])
            else:
                graph_details[m].append(each_graph_details[m])
   
    return graph_details
        
    
    
    
def learning_curve(result1, result2):
    
    # PLOT FOR EACH DATASET QUESTION 1
    
    amazon1_x = result1[0][0]
    amazon1_y = result1[0][1]
    amazon1_ysd = result1[0][2]
    amazon0_x= result2[0][0]
    amazon0_y= result2[0][1]
    amazon0_ysd= result2[0][2]
    
    imdb1_x = result1[1][0]
    imdb1_y = result1[1][1]
    imdb1_ysd = result1[1][2]
    imdb0_x= result2[1][0]
    imdb0_y= result2[1][1]
    imdb0_ysd= result2[1][2]
    
    yelp1_x = result1[2][0]
    yelp1_y = result1[2][1]
    yelp1_ysd = result1[2][2]
    yelp0_x= result2[2][0]
    yelp0_y= result2[2][1]
    yelp0_ysd = result2[2][2]
    

    
    plot1 = plt.figure(1)
    plt.plot(amazon1_x, amazon1_y, label = "m = 1")
    plt.errorbar(amazon1_x, amazon1_y,
             yerr = amazon1_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Amazon Dataset Learning Curve for m = 1')
    plt.legend()
    plt.show()
    
    
    
    plot2 = plt.figure(2)
    plt.plot(amazon0_x, amazon0_y, label = "m = 0")
    plt.errorbar(amazon0_x, amazon0_y,
             yerr = amazon0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Amazon Dataset Learning Curve for m = 0')
    plt.legend()
    plt.show()
    
    
    
    plot3 = plt.figure(3)
    plt.plot(amazon1_x, amazon1_y, label = "m = 1")
    plt.errorbar(amazon1_x, amazon1_y,
             yerr = amazon1_ysd, 
             fmt ='o')
    plt.plot(amazon0_x, amazon0_y, label = "m = 0")
    plt.errorbar(amazon0_x, amazon0_y,
             yerr = amazon0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Amazon Dataset Learning Curve for m = 1 & m = 0')
    plt.legend()
    plt.show()
    
    plot4 = plt.figure(1)
    plt.plot(imdb1_x, imdb1_y, label = "m = 1")
    #plt.errorbar(imdb1_x, imdb1_ysd)
    plt.errorbar(imdb1_x, imdb1_y,
             yerr = imdb1_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('IMDB Dataset Learning Curve for m = 1')
    plt.legend()
    plt.show()
    
    
    
    plot5 = plt.figure(2)
    plt.plot(imdb0_x, imdb0_y, label = "m = 0")
    #plt.errorbar(imdb0_x, imdb0_ysd)
    plt.errorbar(imdb0_x, imdb0_y,
             yerr = imdb0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('IMDB Dataset Learning Curve for m = 0')
    plt.legend()
    plt.show()
    
    
    
    plot6 = plt.figure(3)
    plt.plot(imdb1_x, imdb1_y, label = "m = 1")
    plt.errorbar(imdb1_x, imdb1_y,
             yerr = imdb1_ysd, 
             fmt ='o')
    plt.plot(imdb0_x, imdb0_y, label = "m = 0")
    plt.errorbar(imdb0_x, imdb0_y,
             yerr = imdb0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('IMDB Learning Curve for m = 1 & m = 0')
    plt.legend()
    plt.show()
    
    
    plot7 = plt.figure(1)
    plt.plot(yelp1_x, yelp1_y, label = "m = 1")
    plt.errorbar(yelp1_x, yelp1_y,
             yerr = yelp1_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Yelp Dataset Learning Curve for m = 1')
    plt.legend()
    plt.show()
    
    
    
    plot8 = plt.figure(2)
    plt.plot(yelp0_x, yelp0_y, label = "m = 0")
    plt.errorbar(yelp0_x, yelp0_y,
             yerr = yelp0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Yelp Dataset Learning Curve for m = 0')
    plt.legend()
    plt.show()
    
    
    
    plot9 = plt.figure(3)
    plt.plot(yelp1_x, yelp1_y, label = "m = 1")
    plt.errorbar(yelp1_x, yelp1_y,
             yerr = yelp1_ysd, 
             fmt ='o')
    plt.plot(yelp0_x, yelp0_y, label = "m = 0")
    plt.errorbar(yelp0_x, yelp0_y,
             yerr = yelp0_ysd, 
             fmt ='o')
    plt.xlabel('Train Set Size')
    plt.ylabel('Accuracy')
    plt.title('Yelp Dataset Learning Curve for m = 1 & m = 0')
    plt.legend()
    plt.show()
    
    
    
def cross_valid(result3): 
    
    # PLOT FOR EACH DATASET QUESTION 2
    
    x1 = []
    amazon_y1 = []
    imdb_y1 = []
    yelp_y1 = []
    
    amazon_y1_sd = []
    imdb_y1_sd = []
    yelp_y1_sd = []
    
    
    for key,value in result3.items():
        
        x1.append(key)
        amazon_y1.append(sum(value[0])/10)
        variance_y1 = sum([((each_sample - sum(value[0])/10) ** 2) for each_sample in value[0]]) / len(value[0])
        amazon_y1_sd.append(math.sqrt(variance_y1))
        variance_y2 = sum([((each_sample - sum(value[1])/10) ** 2) for each_sample in value[1]]) / len(value[1])
        imdb_y1_sd.append(math.sqrt(variance_y2))
        variance_y3 = sum([((each_sample - sum(value[2])/10) ** 2) for each_sample in value[2]]) / len(value[2])
        yelp_y1_sd.append(math.sqrt(variance_y2))
        #print(variance_y1)
        #print("ok")
        
        #variance = sum([((each_sample - mean) ** 2) for each_sample in each_graph_details[m]]) / len(each_graph_details[m])

        
        
        imdb_y1.append(sum(value[1])/10)
        yelp_y1.append(sum(value[2])/10)
        
    plt.plot(x1, amazon_y1, label = "Function of m")
    plt.errorbar(x1, amazon_y1,
             yerr = amazon_y1_sd, 
             fmt ='o')
    plt.xlabel('m')
    plt.ylabel('Accuracy')
    plt.title('Amazon Dataset For different m')
    plt.legend()
    plt.show()
    
    plt.plot(x1, imdb_y1, label = "Function of m")
    plt.errorbar(x1, imdb_y1,
             yerr = imdb_y1_sd, 
             fmt ='o')
    plt.xlabel('m')
    plt.ylabel('Accuracy')
    plt.title('IMDB Dataset For different m')
    plt.legend()
    plt.show()
    
    plt.plot(x1, yelp_y1, label = "Function of m")
    plt.errorbar(x1, yelp_y1,
             yerr = yelp_y1_sd, 
             fmt ='o')
    plt.xlabel('m')
    plt.ylabel('Accuracy')
    plt.title('Yelp Dataset For different m')
    plt.legend()
    plt.show()
    
    
     
        
        
if __name__ == "__main__":
    result1 = naive(1)
    result2 = naive(0)
    learning_curve(result1, result2)
    
    m = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
    
    result3 = smoothing_param(m)
    
    cross_valid(result3)
   
    
  