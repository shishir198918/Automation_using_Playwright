@HIM_Dashboard
Feature:Testing data validation

    Scenario: Tesing default episodes presenting on HIM dashboard and validating UI with total number of episodes
        Given login into enviroment as per directed 
            When Goto Him_dashboard where list of episode is shown
            Then Match value with UI to API

    Scenario Outline: Testing episodes presenting on HIM dashboard and validating UI with API
        Given Login into environment go to HIM dashboard
            When Into HIM dashboard go to <assign_coder> selecting
            Then validate data with API with element Total Episode, Uncoded, Unassigned and In progress

    Examples:
        | assign_coder |
        | sai          |
        | sagar        |
        | amrutha      |
                  


