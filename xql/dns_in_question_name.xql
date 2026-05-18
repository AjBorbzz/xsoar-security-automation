datamode dataset = xdr_data 
| filter xdm.network.dns.dns_question.name in ("<*DOMAIN NAME*>")
| fields _time,
xdm.network.dns.dns_question.name,
xdm.source.ipv4,
xdm.source.port,
xdm.target.ipv4,
xdm.target.port,
xdm.event.type,
xdm.event.outcome,
xdm.observer.action,
xdm.observer.product,
xdm.event.operation
| limit 100
| sort desc _time