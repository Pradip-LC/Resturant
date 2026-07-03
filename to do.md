~~@login~~

bootstrap for easy design
flask-sqlacodegen mysql+pymysql://root@localhost/foodbook --flask --outfile models.py
~~@sign up~~

~~-user~~

~~-restaurant~~



~~@forget password~~

~~-verify mail~~

~~-enter token~~

~~-enter new password~~



@Home page(user)

\-load items

\-@search

\-category

\-@profile

\-@view cart

\-add to cart

{

&#x09;@search(after)

&#x09;-results

&#x09;-filter



&#x09;@profile(same for restaurant and user)

&#x09;-details(view only)

&#x09;-fill address(user only)



&#x09;@view cart

&#x09;-remove items

&#x09;-increase/decrease quantity

&#x09;-proceed to payment(verify address)

}



@(restaurant)landing page

\-reviewing(handled by admin, no access till verified)

\-@profile

\-@orders

\-@manage items

\-@report

{

&#x09;@order

&#x09;-pending items(accept, cancel)

&#x09;-processing items(accepted, preparing, on-way/waiting, order complete)

&#x09;-completed items(today only)



&#x09;@manage items

&#x09;-view items

&#x09;-@add items

&#x09;-remove items

&#x09;-@edit items

&#x09;{

&#x09;	@add items

&#x09;	-fill data

&#x09;	-add picture

&#x09;	-publish

&#x09;		

&#x09;	@edit items

&#x09;	-edit data

&#x09;	-add/remove picture(min 1 pic present)

&#x09;	-update

&#x09;}



&#x09;@report

&#x09;-todays/weeks/months completed sales

&#x09;-canceled orders today

&#x09;-total item sold today/week/month

}



@admin access

\-@Account requests

\-@search account

\-@place update/notice/promotion

