import unittest
import datetime

import models

class TestModelCreation(unittest.TestCase):

    def setUp(self):
        self.date1 = datetime.date(2013, 9, 25)
        self.date2 = datetime.date(2014, 2, 12)
    
    def test_user_creation(self):
        usr = models.User("Bob", "Marley")
        self.assertIsInstance(usr, models.User)

    def test_user_keyword_creation(self):
        usr = models.User(name="Vicky", surname="Vouloutsi")
        self.assertIsInstance(usr, models.User)
    
    def test_principal_creation(self):
        prc = models.Principal("John", "Snow", "18097129831")
        self.assertIsInstance(prc, models.Principal)

    def test_prinicipal_keyword_creation(self):
        prc = models.Principal(name="John", surname="Edwards", afm="12321312")
        self.assertIsInstance(prc, models.Principal)

    def test_litigation_creation(self):
        lit = models.Litigation()
        self.assertIsInstance(lit, models.Litigation)
        
    def test_opposition_creation(self):
        opp = models.Opposition()
        self.assertIsInstance(opp, models.Opposition)
    
    def test_nperson_creation(self):
        james = models.NPerson("james", "Joyce", "William", "098732812", "Orelia", "28971739812")
        self.assertIsInstance(james, models.NPerson)

    def test_nperson_keyword_creation(self):
        jim = models.NPerson(name="Jim", surname="Sturgess", father_name="Alex",
                                    afm="8923723")
        self.assertIsInstance(jim, models.NPerson)

    def test_entity_creation(self):
        ibm = models.Entity("International Business Machines", "31879712983", "Langley, Virginia")
        self.assertIsInstance(ibm, models.Entity)
        
    def test_entity_keyword_creation(self):
        ibm = models.Entity(name="International Business Machines", brandname="IBM",
                            base="Langley, Virginia", afm="8091273923")
        self.assertIsInstance(ibm, models.Entity)

    def test_application_creation(self):
        app = models.Application(self.date1)
        self.assertIsInstance(app, models.Application)

    def test_contact_info_creation(self):
        info = models.ContactInfo("Marchmont Cr. 24, Marchmont", "Edinburgh", "004428731893712",
                                  "jamesHolden@yahoo.co.uk")
        self.assertIsInstance(info, models.ContactInfo)

    def test_contact_info_keyword_creation(self):
        info = models.ContactInfo(address="Προπυλαίων 43, Κουκάκι", city="Αθήνα",
                                  mobile="6984232921", email="mitsos@gmail.com")
        self.assertIsInstance(info, models.ContactInfo)


class TestModelCreationFailure(unittest.TestCase):
    def setUp(self):
        pass

    def test_user_failed_creation(self):
        self.assertRaises(TypeError, models.User, "blue")

    def test_user_failed_keyword_creation(self):
        self.assertRaises(TypeError, models.User, penis="small", confidence="low")

    def test_principal_failed_creation(self):
        self.assertRaises(TypeError, models.Principal, "cock", "block")

    def test_principal_failed_keyword_creation(self):
        self.assertRaises(TypeError, models.Principal, cat="Curious", shroedinger="dead")

    def test_litigation_failed_creation(self):
        self.assertRaises(TypeError, models.Litigation, "no need for arguments here")
    
    def test_opposition_failed_creation(self):
        self.assertRaises(TypeError, models.Opposition, "neither here")
        
    def test_application_failed_creation(self):
        self.assertRaises(TypeError, models.Application, "one argument is expected", "not two" )

    def test_application_failed_not_date_argument_creation(self):
        self.assertRaises(TypeError, models.Application, "A date object is expected here")

    def test_nperson_failed_cretion(self):
        self.assertRaises(TypeError, models.NPerson, "way", "to", "go")

    def test_nperson_failed_keyword_creation(self):
        self.assertRaises(TypeError, models.NPerson, this="attribute", does="not", exist="normally")

    def test_entity_failed_creation(self):
        self.assertRaises(TypeError, models.Entity, "shit", "faced")

    def test_entity_failed_keyword_creation(self):
        self.assertRaises(TypeError, models.Entity, testing="tiring", but="useful")

    def test_contact_info_failed_creation(self):
        self.assertRaises(TypeError, models.ContactInfo, "wow", "almost done")
    
    def test_contact_info_failed_keyword_creation(self):
        self.assertRaises(TypeError, models.ContactInfo, i="am", almost="invincible")


class TestLitigationAndOpposition(unittest.TestCase):
    def setUp(self):
        self.date1 = datetime.date(2014, 2, 12)
        self.application1 = models.Application(self.date1)
        self.nperson1 = models.NPerson("John", "Snow", "Alex", "39048703")
        self.nperson2 = models.NPerson("Alex", "Mao", "Brian", "98712398")
        self.entity1 = models.Entity("IBM", "Virginia", "131312331")
        self.entity2 = models.Entity("Microsoft", "California", "983273982")
        self.unconnected_litigation = models.Litigation()
        self.unconnected_opposition = models.Opposition()
        
    def test_connecting_unconnected_litigation_to_entity(self):
        self.assertTrue(self.unconnected_litigation.connect_to_Entity(self.entity1))
    
    def test_connecting_connected_litigation_to_entity(self):
        connected_litigation = self.unconnected_litigation
        connected_litigation.connect_to_Entity(self.entity1)
        self.assertFalse(connected_litigation.connect_to_Entity(self.entity2))

    def test_connecting_unconnected_litigation_to_nperson(self):
        self.assertTrue(self.unconnected_litigation.connect_to_NPerson(self.nperson1))

    def test_connecting_connected_litigation_to_nperson(self):
        connected_litigation = self.unconnected_litigation
        connected_litigation.connect_to_NPerson(self.nperson1)
        self.assertFalse(connected_litigation.connect_to_NPerson(self.nperson2))

    def test_connecting_unconnected_litigation_to_garbage_entity_(self):
        self.assertFalse(self.unconnected_litigation.connect_to_Entity("adasd"))

    def test_connecting_unconnected_opposition_to_entity(self):
        self.assertTrue(self.unconnected_opposition.connect_to_Entity(self.entity))
    
    def test_connecting_connected_opposition_to_entity(self):
        connected_opposition = self.unconnected_opposition
        connected_opposition.connect_to_Entity(self.entity1)
        self.assertFalse(connected_opposition.connect_to_Entity(self.entity2))

    def test_connecting_unconnected_opposition_to_nperson(self):
        self.assertTrue(self.unconnected_opposition.connect_to_NPerson(self.nperson1))

    def test_connecting_connected_opposition_to_nperson(self):
        connected_opposition = self.unconnected_opposition
        connected_opposition.connect_to_NPerson(self.nperson1)
        self.assertFalse(connected_opposition.connect_to_NPerson(self.nperson2))

    def test_connecting_unconnected_opposition_to_garbage_entity_(self):
        self.assertFalse(self.unconnected_opposition.connect_to_Entity("adasd"))

if __name__ == '__main__':
    unittest.main()

    
