Feature: VF-IS branding UI differences from vanilla Kolibri release

	Scenario: Check required languages for VF-IS Kolibri
		Given that I am on VF-IS Kolibri sign-in page in English
			And I see the options to change language to French, Portuguese, and Kiswahili
		When I click the option for Portuguese
		Then I see the sing-in page in Portuguese
		When I click the option for French
		Then I see the sing-in page in French
		When I click the option for Kiswahili
		Then I see the sing-in page in Kiswahili

	Background:
    Given that I am signed into VF-IS Kolibri 

  	Scenario: Account vs. Profile
  		When I open the user menu in the upper right corner
  		Then I see *Account* item under the user type # instead of *Profile* in vanilla Kolibri
      	And I see the *About* item below
      When I click *Account* item option
      Then I am on the *Account* page
      	And I see my *Points*, *User type*, and *Full name*
      		But I don't see neither *Facility* nor *Username* # as I would in vanilla Kolibri

    Scenario: Instant Schools in the sidebar
    	When I open the sidebar
    	Then I see *Instant Schools* on top  # instead of *Kolibri* in vanilla release

  Background:
    Given that I am NOT signed into VF-IS Kolibri

    Scenario: Land on *About* page when accessing as a guest
    	Given that I am on VF-IS Kolibri sign-in page
	    	When I click the *Access as guest* button
	    	Then I see the the *About* page
    		When I click the *Start learning* button 
    		Then I see the *Learn > Channels* page


