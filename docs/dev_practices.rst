ASTT software Dev Practices
===========================

**Running the unit tests locally**

* Run the unit tests

    ``` python -m unittest discover -v -s tests/unit ```

**Running the acceptance tests locally**

* Build your changes into a docker container
  
    ```docker build -t astt-cam-software . ```

* Start VCAN Network
  
    ```sudo sh startVirtualCANInterface.sh ```

* Run the simulator
  
    ``` docker run -d --network=host <astt image id> ``` or  ``` docker run -d --network=host astt-cam-software:latest ```

* Run Acceptance Tests
    ``` pytest tests/acceptance -v ```


**Building the docs locally**

* To build the docs,first go to the directory where conf.py exists.
    ```cd docs ```

* Generate the readthedocs pages
    ```sphinx-build -b html . _build -v ```

* The home page of the docs is found in _build directory,open the index.html with the browser.
  
**Branching on github**

* All developers are supposed to branch from the main branch in order to add more work.
  examples:

   main --> astt-80-add-stow-button

   main --> astt-91-integrate-point-function-to-gui
   
   main --> astt-107-update-docs

* To Branch, ensure you are on the main branch
   
   ```git checkout main```

* checkout to your new branch which you will use for adding new changes
   
   ```git checkout -B astt-<Jira number>-<Jira ticket title>```

* Once done adding new changes, open an pull request.The pull request is then merged to main
   
   astt-107-update-docs --> main
