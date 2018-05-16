from aylienapiclient import textapi

client = textapi.Client(" 51c406ea", " 06f281d46fe40eac69fcbd4170ca9b33")



text = "Typical McDonalds with your typical menu and food. The bathrooms and eating areas are decently clean as well."
"Service has improved over the past few years now that they have a order food counter side and a pick up side. This makes it so there's less people crowding around the counter space."
"Only complaint is line management and that ordering food is kind of slow. I think there should just be one central line (like Whole Foods) to make things more efficient because it sucks when you've been waiting on line for a long time and your line is not moving while people who just entered in the store wait on another line and are served before you."
"Also the employees joke around too much behind the counter which is inefficient when there are long lines."

absa = client.AspectBasedSentiment({'domain': 'restaurants', 'text': text})
for aspect in absa['aspects']:
  print(aspect)
