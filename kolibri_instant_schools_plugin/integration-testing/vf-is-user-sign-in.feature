Feature: User sign-in
    IS subscribers should be able to sign in to access Kolibri
    If the simplified sign-in setting is on, user should be able to sign in only with their mobile number
    If the user account is registered correctly, they should arrive at the *Learn > Channels* page upon sign-in

  Background:
    Given that I am on the Kolibri sign-in page
      And that there is a registered user with <mobile-number> and password <password>

    Scenario: Normal sign-in
      When I fill out my mobile <mobile-number>
        And I fill out my password <password>
        And I click the *Sign in* button 
      Then I am signed in and I can see the *Learn > Channels* page

    Scenario: Simplified sign-in
      Given that simplified sign-in facility setting is on
        When I fill out my mobile <mobile-number>
          And I click the *Sign in* button 
        Then I am signed in and I can see the *Learn > Channels* page

  Examples:
  | mobile-number | password      |
  | 123456789123  | 123456789123  |