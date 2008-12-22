===========
Scalability
===========

The Moksha architecture is designed from the ground up to be highly scalable, through a variety of different ways.

Extensive caching
-----------------

By facilitating extensive server and client side caching, moksha allows
applications to scale "out of the box".


Scalable databases
------------------

Moksha transparently handles creating the SQLAlchemy engines and handing them
off to your application.  This allows Moksha to create separate, isolated,
sharded, databases for each application to live in.  This gives Moksha the
ability to horizontally and vertically scale applications as needed.


Scalable components
-------------------

The architecture is designed in a way that makes it extremely scalable yet flexible.  This means that you could potentially run the entire platform on your laptop, or within a cloud.

The following architecture components can be made redundant to scale in a
production environment:

- WSGI/TG2 frontends
- Orbited proxies
- Qpid brokers
- Feed fetchers / Data pollers
- memcached daemons
- Databases