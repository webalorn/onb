import onb, env.dev.settings

dynI18n = onb.dyndb.get('i18n')

id1 = dynI18n.new(1, 'fr', 'Mon texte1')
id2 = dynI18n.new(1, 'fr', 'Mon texte2')
id3 = dynI18n.new(1, 'fr', 'My text')

t = dynI18n.getMultiple([id1, id2, id3, 'db'], 'fr')
print(t)