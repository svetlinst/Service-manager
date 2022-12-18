# Service Manager Project

[Link to the deployed dev version on AWS](https://servicesmanager.net/en/ "AWS")

*If you'd like to play around with the application and test it in development environment, please register an account and send me an e-mail using the "Contact Us" forms so I could add your user to a Group and enable the application for you.*

- The goal of the application is to be utilized by a service entity (company), a repair workshop, or any other entity that provides asset/device service to their clients.

## Admin panel access
- Super users (is_superuser) and Staff (is_staff) are allowed to open the admin panel.
- Super users have full control
- Staff members cannot view nor modify App user permissions.

## User registration
- When a user gets registered, they are not automatically associated with a group.
- Then, a superuser has to add the new user to one (or more) of the 3 permission groups (Front office, Back office, Master data).
- Front office - this role handles the creation of service orders and managing customer information.
- Back office - handles the servicing of orders and assigns the required materials.
- Master data - has control over Assets, Brands, Categories, Materials, etc. Keeps up-to-date with the master data of the application.

## Object entities (tables)

[The database diagram could be found here.](https://github.com/svetlinst/Service-manager/blob/master/service_manager/db_diagram.jpg "Diagram")

#### Master data:
- Brand - this is a simple table that serves the purpose of keeping all different device brands/make into a neat normalized entity (example: HP, Dell, Canon, Xerox, etc.)
- Asset - this is a one-level-down, more granular entity, where each asset is linked to a Brand, and assosiated with a Model Number and Name. The Assets are grouped into Asset Categories. (example: Laptop HP Envy 121).
- Asset Category - grouping hierarchy of assets (example: Laptops, Desktops, Laser Printers, MFCs, etc.).
- Material - this is the general entity that is assigned to the orders that are serviced. It could be a part, consumable, labor, travel, etc. This is the item that has to be billed to the customer once the order is serviced and finalized (example: 1hr effort, mid-level technician).
- Material Category - grouping hierarchy of assets (example: Labor).

#### Customer entities
- Customer Asset - this is an asset associated with a given customer. To distinguish between the generic asset (which is just a master data element), the asset is tied to a customer. It also has Serial and Product numbers assigned that guarantee its uniqueness. The Customer assets are at the core of managing the Service orders due to being the object that is being serviced.
- Customer - the customers are the main point of reference in the application. There are 2 types of customers - Business and Individual. Departments could be added for Business customers (for example customer "High Tech Inc." could have departments "Accounting" and "Sales"). Also, Customer representatives could be linked to Customers (for example "High Tech Inc." could have Jonh Doe and Marry Jane as customer representatives that would handle the handing over and collecting of the company's assets).
- Customer Type - this is the type of customer being Business or Individual. Individual customers and not tied to a company hence they don't have Departments nor Representatives.

#### Service orders
- Service Order Header - this is the entity that keeps track of the servicing progress of the customer's assets. There are various timestamps capturing information around: when an order is created, then it is serviced and finalized. It also keeps track of who accepted the order, serviced it, and returned it.
- Service Order Detail - this table contains the items (materials) associated with the service order by the respective employee. The application calculates the amount due based on this information.
- Service Order Notes - this entity keeps track of all notes created by employees throughout the lifecycle of each service order.


## Django features utilized:
1. Soft delete - the "ActiveModel" abstract class prevents records from deletion. When delete is triggered (both in the application itself and in the admin panel), the flag "active" gets changed to False and no deletion is performed. This prevents the accidental (or on purpose) removal of important information. There is a custom manager (used as default in the application), that prevents showing the soft-deleted records in the app All models that inherit this class have another manager that could retrieve the soft-deleted records as well.
2. Audit base abstract entity saving information around record creation and last update date.
3. Sending e-mail messages async via celery (Contact us form, when Service order header is created, upon e-mail password reset).
4. The application is deployed on AWS and fully functional.
5. Extend the base Application user with additional Profile information. Enabled password reset over e-mail via a token.
6. Internationalization and Localization (Bulgarian added as a supported language).
7. Created 3 user Groups in migration (so they don't have to be recreated manually) along with the respective access permissions.
8. Opening a link that requires authentication, before login, redirects the user to the login page, and in case that's successful - properly redirects back to the initial link that the user requested.
9. Integration tests for the two major apps - Main (Service order handling) and Customers.
10. Utilized Bootstrap's modal forms on several occasions.
11. Template inheritance.
12. Pagination - works properly even when combined with search query parameters
13. Custom admin features - Service Order Header admin.
14. Django messages - when sending a Contact us e-mail.

