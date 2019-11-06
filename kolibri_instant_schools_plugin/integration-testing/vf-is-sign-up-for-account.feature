Feature: Vodafone subscriber signs up for an account
    Vodafone subscribers should be able to sign up for the IS Kolibri account, if permitted by respective facility setting

  Background:
    Given that *Allow learners to create accounts* setting is activated in *Facility > Settings*
      And that I am on the Kolibri sign-in page

  Scenario: Sign up for an account
    When I click *Create an account* button
    Then I am on *Create an account* page
    When I fill out my full name <full_name>
     And I fill out my mobile number <mobile-number>
     And I fill out my password <password>
     And I activate the checkbox for the Terms of service
     And I click the *Finish* button 
    Then I am on the the *About* page
    When I click the *Start learning* button 
    Then I see the *Learn > Channels* page

  Scenario: Mobile number is already registered
    Given A user already exists with mobile number <mobile-number>
    When I try to sign up for a new account with the same mobile number <mobile-number>
    Then I get a validation message shown next to the *Phone number* field 'An account with that phone number already exists'

  Scenario: Incorrect number of mobile digits
    Given I am on *Create an account* page
    When I enter a mobile number with less then 9 digits
    Then I see the error notification *A valid phone number has at least 9 digits* below the field 

  Examples:
  | mobile-number | password      |
  | 123456789123  | 123456789123  |