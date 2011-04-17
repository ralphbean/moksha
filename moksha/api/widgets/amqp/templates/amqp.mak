<script type="text/javascript">

if (typeof moksha_amqp_conn == 'undefined') {
	moksha_callbacks = new Object();
	moksha_amqp_remote_queue = null;
	moksha_amqp_queue = null;
	moksha_amqp_on_message = function(msg) {
		var dest = msg.header.delivery_properties.routing_key;
		var json = null;
		try {
			var json = $.parseJSON(msg.body);
		} catch(err) {
			moksha.error("Unable to decode JSON message body");
			moksha.error(msg);
		}
		if (moksha_callbacks[dest]) {
			for (var i=0; i < moksha_callbacks[dest].length; i++) {
				moksha_callbacks[dest][i](json, msg);
			}
		}
	}
}

## Register our topic callbacks
% for topic in w.topics:
	var topic = "${topic}";
	if (!moksha_callbacks[topic]) {
		moksha_callbacks[topic] = [];
	}
	moksha_callbacks[topic].push(function(json, frame) {
		${w.onmessageframe[topic]}
	});
% endfor

## Create a new AMQP client
if (typeof moksha_amqp_conn == 'undefined') {
	document.domain = document.domain;
	$.getScript("${w.orbited_url}/static/Orbited.js", function() {
		Orbited.settings.port = ${w.orbited_port};
		Orbited.settings.hostname = '${w.orbited_host}';
		Orbited.settings.streaming = true;
		moksha_amqp_conn = new amqp.Connection({
			% if w.send_hook:
				send_hook: function(data, frame) { ${w.send_hook} },
			% endif
			% if w.recieve_hook:
				recive_hook: function(data, frame) { ${w.recieve_hook} },
			% endif
			host: '${w.amqp_broker_host}',
			port: ${w.amqp_broker_port},
			username: '${w.amqp_broker_user}',
			password: '${w.amqp_broker_pass}',
		});
		moksha_amqp_conn.start();

		moksha_amqp_session = moksha_amqp_conn.create_session(
			'moksha_socket_' + (new Date().getTime() + Math.random()));

		moksha_amqp_remote_queue = 'moksha_socket_queue_' +
				moksha_amqp_session.name;

		moksha_amqp_session.Queue('declare', {
				queue: moksha_amqp_remote_queue
		});
		moksha_amqp_queue = moksha_amqp_session.create_local_queue({
				name: 'local_queue'
		});

		% if w.onconnectedframe:
			${w.onconnectedframe}
			moksha_amqp_queue.start();
		% endif

	});

} else {
	## Utilize the existing Moksha AMQP socket connection
	${w.onconnectedframe}
	moksha_amqp_queue.start();
}

if (typeof moksha == 'undefined') {
	moksha = {
		/* Send an AMQP message to a given topic */
		send_message: function(topic, body) {
			moksha_amqp_session.Message('transfer', {
				accept_mode: 1,
				acquire_mode: 1, 
				destination: 'amq.topic',
				_body: $.toJSON(body),
				_header: {
					delivery_properties: {
						routing_key: topic
					}
				}
			});
		},
	}
}
</script>
