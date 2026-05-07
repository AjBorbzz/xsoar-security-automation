datamodel dataset in (xdr_data)
| filter XDM_ALIAS.domain != null
| fields
    _time,
    fieldset.xdm_network,
    XDM_ALIAS.domain,
    xdm.network.http.domain,
    xdm.network.dns.dns_question.name,
    xdm.network.dns.dns_resource_record.name,
    xdm.source.identity.domain,
    xdm.target.identity.domain,
    xdm.intermediate.identity.domain,
    xdm.auth.ntlm.dns_domain,
    xdm.auth.ntlm.domain
| sort desc _time
| limit 100