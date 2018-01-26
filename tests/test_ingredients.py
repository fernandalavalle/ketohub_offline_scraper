import unittest

from scraper import ingredients


class ParseIngredientTest(unittest.TestCase):

    def test_parse_ingredient(self):
        cases = (
            (u'2.5 ounces (\u00bc whole) cucumber, seeded and grated',
             'cucumber'),
            ('1 (15-oz) can Ro*Tel', 'Ro*Tel'),
            ('1 2/3 cup canned coconut milk', 'coconut milk'),
            (u'3 tablespoons Rao\u2019s marinara', 'Rao\'s marinara'),
            (u'1/4 tsp. garlic\u00a0powder', 'garlic powder'),
            (u'\u00bc cup heavy whipping cream', 'heavy whipping cream'),
            (u'\u00be cup grated Parmesan', 'grated Parmesan'),
            (u'\u2153 cup sugar free ketchup', 'sugar free ketchup'),
            (u'4 medium jalape\u00f1o peppers (56 g)',
             'medium jalapeno peppers'),
            (u'\u201cBest Low Carb\u201d tortillas',
             '"Best Low Carb" tortillas'),
            (u'8 oz Cheddar Shredded \u2013 Mild', 'Cheddar Shredded - Mild'),
            (u'12 slices of NatureRaised Farms\xae Bacon', 'Bacon'),
            ('10.5 ounces (300 g) sugar-free dark chocolate',
             'sugar-free dark chocolate'),
            ('3 oz. / 85g cold butter', 'cold butter'),
            ('2 cups / 16 fl oz. / 1 pint chicken stock', 'chicken stock'),
            ('8 fl. oz / 1 cup chicken stock', 'chicken stock'),
            ('1 lb / 450g assorted wild mushrooms (I used shiitake and cremini), stemmed and quartered',
             'assorted wild mushrooms, stemmed and quartered'),
            ('2 garlic cloves, finely minced', 'garlic cloves, finely minced'),
            ('1/2 cup shredded Colby jack cheese, separated in 1/4 cups',
             'shredded Colby jack cheese'),
            ('Pinch of cayenne pepper', 'cayenne pepper'),
            ('1 4.5oz can chopped green chiles', 'chopped green chiles'),
            ('3 oz. / 85g cold butter', 'cold butter'),
            ('1 teaspoon butter, for greasing the pan', 'butter'),
            ('Salt to taste', 'Salt'),
            ('Optional: 1/2 teaspoon vanilla extract', 'vanilla extract'),
            ('16 ounces cream cheese, room temperature', 'cream cheese'),
            ('1/4 cup thinly sliced scallions, plus more for garnish, if desired',
             'thinly sliced scallions, plus more for garnish'),
            ('6 tablespoons ghee*', 'ghee'),
            ('6 tablespoons ghee* (if fully dairy free, use coconut oil)',
             'ghee'),
            ('1 oz coconut oil', 'coconut oil'),
            ('1 oz. coconut oil', 'coconut oil'),
            ('1 pound ground chorizo', 'ground chorizo'),
            ('4 ounces smoked salmon', 'smoked salmon'),
            ('4 ounces 85% dark chocolate', '85% dark chocolate'),
            ('3.80 lb(s), boneless beef chuck roast',
             'boneless beef chuck roast'),
            ('1 cup chopped pecans', 'chopped pecans'),
            ('1 Cup (8oz) Cubed Mozzarella', 'Cubed Mozzarella'),
            ('1/4 Cup Pesto', 'Pesto'),
            ('3 cups (321 g) cauliflower rice', 'cauliflower rice'),
            ('7 slices (56.7) of cooked bacon', 'cooked bacon'),
            ('1 cup of sliced ham', 'sliced ham'),
            ('3 stalks celery', 'celery'),
            ('12 (1-inch) cubes smoked cheddar cheese',
             'smoked cheddar cheese'),
            ('5 medium Chicken Thighs (~28 oz.)', 'medium Chicken Thighs'),
            ('12 (1-ounce) sausage patties', 'sausage patties'),
            ('4 Chicken Breasts', 'Chicken Breasts'),
            ('1 avocado, sliced or cubed', 'avocado, sliced or cubed'),
            ('3 Tbsp. Olive Oil', 'Olive Oil'),
            ('1 tablespoon lemon zest', 'lemon zest'),
            ('1 tsp. Garlic', 'Garlic'),
            ('~1 tsp. Absorbed Bacon Fat', 'Absorbed Bacon Fat'),
            ('1 teaspoon sage', 'sage'),
            ('1/8 teaspoon. salt', 'salt'),
            ('3 tbsp. + 1 tsp. Olive Oil', 'Olive Oil'),
            ('1 teaspooon Garlic', 'Garlic'),
            ('1 inch Ginger Root, grated', 'Ginger Root, grated'),
            ('2 cloves garlic', 'garlic'),
            ('2 cloves (6 g) garlic,peeled', 'garlic'),
            ('2 Sprigs Fresh Thyme', 'Fresh Thyme'),
            ('5 bars Chocoperfection', 'Chocoperfection'),
            ('1 head cabbage thinly sliced', 'cabbage thinly sliced'),
            ('1 bar (10g) Chocoperfection Dark Chocolate',
             'Chocoperfection Dark Chocolate'),
            ('2 g fresh oregano', 'fresh oregano'),
            ('Xantham gum', 'xanthan gum'),
            ('150g Halloumi Cheese', 'Halloumi Cheese'),
            ('2 tablespoons soy sauce*', 'soy sauce'),
            ('15 drops liquid stevia', 'liquid stevia'),
            ('1/2 cup water, if needed*', 'water'),
            ('5 pound whole roasted chicken*', 'whole roasted chicken'),
            ('5-6 fresh (2.5 g) basil leaves to garnish', 'fresh basil leaves'),
            ('1 cup Coconut Milk (carton)', 'Coconut Milk'),
            ('3 zucchini squash (1 lb total)', 'zucchini squash'),
            ('1lb ground hot italian sausage', 'ground hot italian sausage'),
            ('1 1/2 lbs. Chicken Thighs, skin on', 'Chicken Thighs, skin on'),
            ('2 scoops Chocolate 100% Casein Protein Powder',
             'Chocolate 100% Casein Protein Powder'),
            ('1 container Wild Oats Organic Tomato Basil Pasta Sauce',
             'Wild Oats Organic Tomato Basil Pasta Sauce'),)
        for raw, expected in cases:
            actual = ingredients.parse(raw)
            self.assertEqual(actual, expected, '[%s] != [%s] (original=[%s])' %
                             (actual, expected, raw))
