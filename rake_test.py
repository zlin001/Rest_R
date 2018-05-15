from rake_nltk import Rake

# EXAMPLE ONE - SIMPLE
stoppath = "SmartStoplist.txt"
r = Rake()
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
       "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
       "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating"\
       " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
       "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
       "systems and systems of mixed types."

r.extract_keywords_from_text(text)
print(r.get_ranked_phrases_with_scores())
