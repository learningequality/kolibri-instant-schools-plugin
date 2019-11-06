Feature: IS Super admin signs-in
    Super admin should be able to sign in to access Kolibri
    If the admin account is registered correctly, they should arrive at the *Facility > Classes* page upon sign-in

  Background:
    Given that I am on the Django administration page of my Kolibri installation (http://127.0.0.1:8080/admin)
      And that there is a Super admin <username> with password <password>

  Scenario: Sign-in
    When I fill out my username <username>
      And I fill out my password <password>
      And I click the *Log in* button 
    Then I am signed in and I can see the Django site administration page
    When I click the *View site* link in the upper right
    Then I can see *Facility > Classes* page # 0.6.3 version landed the admin on the Learn page

  Examples:
  | username | password |
  | admin    | admin    |