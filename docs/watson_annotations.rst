Watson Annotations
==================

For each chat message sent in Watson Workspace many Annotations are generated utilising the Watson APIs to extract
information from the chat message. Whether is it used or not these will be sent with each message, so if there is a
webhook listening in for annotation-added these will have to be ignored,handled or filtered.

There may be some information that is useful for example message-nlp-entities picked out a location which could display
an annotation displaying travel options.

Example
--------

Sending the message **`We need to get this client on the call, it is very important we don't lose them after the San Francisco fiasco`**
To stress, this is a sample sentence.

message-nlp-entities

.. code-block:: javascript

    {"language":"en","entities":[{"count":1,"relevance":0.33,"text":"San Francisco","type":"Location"}]}

Language was picked up, along with the entity San Francisco which is of type Location

message-nlp-keywords

.. code-block:: javascript

    {"language":"en","keywords":[{"relevance":0.903347,"text":"San Francisco fiasco"},{"relevance":0.263684,"text":"client"}]}

Keywords noted were "San Francisco fiasco" and "client"

message-nlp-docSentiment

.. code-block:: javascript

    {"language":"en","docSentiment":{"score":0.488068,"type":"neutral"}}

message-nlp-concepts

.. code-block:: javascript

    {"language":"en","concepts":[{"dbpedia":"http://dbpedia.org/resource/2000s_music_groups","relevance":0.840367,"text":"2000s music groups"},{"dbpedia":"http://dbpedia.org/resource/São_Francisco_(disambiguation)","relevance":0.757086,"text":"São Francisco"}]}

message-nlp-taxonomy

.. code-block:: javascript

    {"language":"en","taxonomy":[{"confident":false,"label":"/business and industrial/advertising and marketing/public relations","score":0.246501},{"confident":false,"label":"/health and fitness/weight loss","score":0.218009},{"confident":false,"label":"/art and entertainment/music/music genres/hip hop","score":0.162234}]}



