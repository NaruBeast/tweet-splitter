def tweet_splitter(text, counter):
    
    char_limit = 280
    counter_char = 8 if counter else 0
    end = char_limit - counter_char
    tweets = []
    break_points = ".,&!?;"  # Sentence ending punctuations
    index = 0
    
    if counter:  # By Punctuation with Counter
        tweets_temp = []  # Temporary list
        count = 1
        
        while (index + end) < len(text):  # If the remaining text still has more than 272 (+8 for counter) characters, we must cut.
            for break_pt in range(index+end-1, index-1, -1):  # From the 280th, go backwards and find the nearest punctuation mark.
                if text[break_pt] in break_points:
                    tweets_temp.append(text[index:break_pt+1].strip() + " ({}/".format(count))  # Append from starting index up to punctuation mark. Since we can't yet find the total number of tweets we will be creating, we'll add the denominator later.
                    index = break_pt+1  # New starting index at the next word
                    break  # Go back to while loop
            else:
                space = text[index:index+end].rfind(' ')
                if space!=-1:
                    tweets_temp.append(text[index:index+space].strip() + " ({}/".format(count))
                    index += (space + 1)
                else:
                    tweets_temp.append(text[index:index+end].strip() + " ({}/".format(count))
                    index += end
            count+=1
                
        tweets_temp.append(text[index:len(text)].strip() + " ({}/".format(count))  # No more cutting needed, append remaining words.
        for tweet in tweets_temp:  # Call all tweets and add the denominator in the counter since we now know the total amount of tweets created. Remember format " ({}/{})".
            tweets.append(tweet + "{})".format(count))

    else:  # By Punctuation without Counter
        while (index + end) < len(text):  # Same thing as above, without the complex counter
            for break_pt in range(index+end-1, index-1, -1):
                if text[break_pt] in break_points:
                    tweets.append(text[index:break_pt+1].strip())
                    index = break_pt+1
                    break
            else:
                space = text[index:index+end].rfind(' ')
                if space!=-1:
                    tweets.append(text[index:index+space].strip())
                    index += (space + 1)
                else:
                    tweets.append(text[index:index+end].strip())
                    index += end
        tweets.append(text[index:len(text)].strip())

    return tweets
