#   1- for word_match func in PFUNCZ we can use spell.candidates instead of spell.correction
#       its obviouse that some changes must be done

#   2- all funcs must be caled in order to finish what started in one step

#   3- in 2 approaches we can apply negative affect of sentences
#       first by calculating the sentence score then reversing
#       second by meddle by reversing each word score
#   [a,b] -> [c,d]
#   (((x-a)/(b-a))*(d-c))+c
