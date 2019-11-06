Feature: Multiple users need to be able to sign in to Kolibri with the same mobile number and select their own profile
    VF-IS plugin allows multiple users to sign in to Kolibri with the same mobile number, and interact with the platform under their own profile
    If they do not have their own profile, they should be able to create one


  Background:
    Given that I am signed in to Kolibri with the mobile number used by multiple users
      And I am on the *Select profile* page

    Scenario: I don't see my own profile
      When I press the *New profile* button
      Then I see the *New profile* modal
      When I write my profile name 
        And I press the *Save* button 
      Then I see the *Select profile* page again
        And I see my profile name in the list

    Scenario: I see my own profile for the first time
      When I click the *Select* button for my profile
      Then I see the *About* page
      When I click the *Start learning* button 
      Then I see the *Learn > Channels* page

    Scenario: I see my own profile for >=2nd time
      When I click the *Select* button for my profile
      Then I see the *Learn > Channels* page
