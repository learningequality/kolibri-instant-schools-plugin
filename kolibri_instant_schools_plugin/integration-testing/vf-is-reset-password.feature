Feature: Users need to be able to reset the password needed to access IS Kolibri

  Background:
    Given that I have an account for IS Kolibri with a mobile number <mobile-number>
      And I am on the Kolibri sign in page
      And I forgot the password <password> used to access my account

    Scenario: Request password reset
      When I click the *Reset your password* link
      Then I see the *Reset password* modal
      When I write my mobile number <mobile-number> 
        And I press the *Send* button 
      Then I see the *SMS sent* message in the modal
      When I check my mobile
      Then I see an SMS with the link to click to reset password

    Scenario: SMS service error
      When I write my mobile number <mobile-number> 
        And I press the *Send* button 
      Then I see the *SMS service error* message in the modal

  Examples:
  | mobile-number | password      |
  | 123456789123  | 123456789123  |