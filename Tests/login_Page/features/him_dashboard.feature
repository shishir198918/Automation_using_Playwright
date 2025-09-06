Feature: Testing the login page 
  Scenario: test a login page 
    Given url for login page provided
     When goto the url for login page entre valid username and password
     Then entre to homepage 
  
  Scenario: Testing with blank user id 
    Given url for login provided
     When goto to the login button click login button 
     Then Alert msg shown for required user_id and password