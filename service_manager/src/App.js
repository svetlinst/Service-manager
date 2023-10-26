import ListGroup from "./components/ListGroup";
import React, { useEffect }  from "react";
import ReactDOM from "react-dom";
import Card from "./components/ui/Card";
import Layout from "./components/layout/Layout";
import Dashboard from "./components/Dashboard";
import ApiClient from "../api-client/src/ApiClient";
// import EnApi from "../api-client/src/api/EnApi";
import { Configuration, EnApi } from "../my-api-client_js/src";
import Cookies from "js-cookie";

function App() {
    var ServiceManagerApi = require("service_manager_api");

    var defaultClient = ServiceManagerApi.ApiClient.instance;

    // Configure API key authorization: cookieAuth
    var cookieAuth = defaultClient.authentications["cookieAuth"];

    cookieAuth.apiKey = Cookies.get('csrftoken');
    // // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    // cookieAuth.apiKeyPrefix['sessionid'] = "Token"


    var api = new ServiceManagerApi.EnApi();
    console.log(api);

    var serviceOrderHeader = new ServiceManagerApi.ServiceOrderHeader(); // {ServiceOrderHeader}
    console.log(serviceOrderHeader)

    useEffect(() => {
        // Make a GET request to list all ServiceOrderHeader objects
        const listServiceOrderHeaders = async () => {
          try {
            // const response = await api.enApiServiceOrderHeadersList();
            const response = await api.enApiServiceOrdersList();
            console.log('List of ServiceOrderHeaders:', response.data);
          } catch (error) {
            console.error('Error listing ServiceOrderHeaders:', error);
          }
        };
    
        listServiceOrderHeaders();
      }, []);

    // var callback = function (error, data, response) {
    //     if (error) {
    //         console.error(error);
    //     } else {
    //         console.log("API called successfully. Returned data: " + data);
    //     }
    // };
    // api.enApiServiceOrdersCreate(serviceOrderHeader, callback);

    // const apiClient = new EnApi(new Configuration({
    //     basePath: 'http://localhost:8000/',
    //     headers: {
    //       'X-CSRFToken': Cookies.get('csrftoken'),
    //     }
    //   }));


    //   apiClient.employeesList().then((result) => {
    //     // do something with employees here - e.g. load them into our UI
    //     console.log('got back employees', result.results);
    //   });

    return (
        <Layout>
            <Dashboard></Dashboard>
        </Layout>
    );
}

export default App;
